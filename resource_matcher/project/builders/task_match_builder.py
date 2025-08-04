import heapq
from user.repositories.user_repository import get_available_employees
from project.repositories.skill_repository import get_skills_by_ids

class TaskMatchBuilder:
    def __init__(self, task, top_k=5):
        self.task = task
        self.top_k = top_k
        self.required_skills = set(task.required_skill.values_list("id", flat=True))
        self.heap = []

    def build(self):
        users = get_available_employees(self.task.start_date, self.task.end_date)

        for user in users:
            user_skill_ids = set(user.skills.values_list("skill_id", flat=True)) # type: ignore
            matched_skills = self.required_skills & user_skill_ids
            unmatched_skills = self.required_skills - user_skill_ids

            if not matched_skills:
                continue

            match_percentage = round((len(matched_skills) / len(self.required_skills)) * 100)
            user_data = {
                "user_id": user.id, # type: ignore
                "email": user.email,
                "name": user.name,
                "match_percentage": match_percentage,
                "matched_skills": list(get_skills_by_ids(matched_skills)),
                "unmatched_skills": list(get_skills_by_ids(unmatched_skills))
            }

            heapq.heappush(self.heap, (match_percentage, user_data))
            if len(self.heap) > self.top_k:
                heapq.heappop(self.heap)

        return sorted([item[1] for item in self.heap], key=lambda x: x["match_percentage"], reverse=True)

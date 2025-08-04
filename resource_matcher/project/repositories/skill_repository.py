from project.models import Skill

def list_all_skills():
    return Skill.objects.all()

def get_skills_by_ids(ids):
    return Skill.objects.filter(id__in=ids).values("id", "name")

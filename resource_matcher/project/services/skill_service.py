from rest_framework.response import Response
from project.repositories.skill_repository import list_all_skills
from project.factories.skill_factory import SkillFactory

def list_skills_service():
    skills = list_all_skills()
    serializer = SkillFactory.get_list_serializer(skills)
    return Response(serializer.data)

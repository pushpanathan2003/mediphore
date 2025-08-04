from project.serializers.skills_serializers import SkillSerializer

class SkillFactory:
    @staticmethod
    def get_list_serializer(skills):
        return SkillSerializer(skills, many=True)

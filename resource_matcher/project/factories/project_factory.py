from project.serializers.project_serializers import ProjectSerializer

class ProjectFactory:
    @staticmethod
    def get_serializer(data, instance=None):
        return ProjectSerializer(data=data, instance=instance)

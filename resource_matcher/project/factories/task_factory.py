from project.serializers.task_serializers import TaskCreateSerializer, TaskSerializer

class TaskFactory:
    @staticmethod
    def get_create_serializer(data):
        return TaskCreateSerializer(data=data)

    @staticmethod
    def get_list_serializer(tasks):
        return TaskSerializer(tasks, many=True)

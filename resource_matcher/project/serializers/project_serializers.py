from rest_framework import serializers

from project.models import Project
from project.serializers.task_serializers import TaskSerializer

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_by', 'tasks']

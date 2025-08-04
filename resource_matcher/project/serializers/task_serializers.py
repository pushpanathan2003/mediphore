from rest_framework import serializers

from project.models import Project, Skill, Task
from project.serializers.skills_serializers import SkillSerializer

class TaskProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']

class TaskCreateSerializer(serializers.ModelSerializer):
    required_skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True
    )

    class Meta:
        model = Task
        fields = ['id', 'name' ,'project', 'start_date', 'end_date', 'required_skill']

class TaskSerializer(serializers.ModelSerializer):
    required_skill = SkillSerializer(many=True, read_only=True)
    project = TaskProjectSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'name', 'start_date', 'end_date', 'project', 'required_skill']

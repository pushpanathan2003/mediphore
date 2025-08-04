from rest_framework import serializers

from project.models import Skill
from project.serializers.skills_serializers import SkillSerializer
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    
    skills = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'available_from', 'available_to', 'skills']
        extra_kwargs = {
            'password': { 'write_only': True },
        }
    def get_skills(self, obj):
        skills = Skill.objects.filter(userskill__user=obj)
        return SkillSerializer(skills, many=True).data
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

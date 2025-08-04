from os import access
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from enum import Enum
from enumchoicefield import EnumChoiceField
from project.models import Skill

class EnumRole(Enum):
    manager = "Manager"
    employee = "Employee"

# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    role = EnumChoiceField(enum_class=EnumRole, null=True)
    available_from = models.DateField(null=True)
    available_to = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'skill')


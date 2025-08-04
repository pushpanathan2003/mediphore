from user.repositories.user_repository import (
    update_user_availability, get_user_skills,
    delete_user_skills, bulk_add_user_skills
)
from user.serializers.user_serializers import UserSerializer
from django.db import transaction

class UserAvailabilityBuilder:
    def __init__(self, user):
        self.user = user
        self.available_from = None
        self.available_to = None
        self.skill_ids = []

    def set_availability_range(self, available_from, available_to):
        self.available_from = available_from
        self.available_to = available_to
        return self

    def set_skills(self, skill_ids):
        self.skill_ids = skill_ids
        return self

    def build(self):
        with transaction.atomic():
            update_user_availability(self.user, self.available_from, self.available_to)

            current_skills = get_user_skills(self.user)
            incoming_skills = set(self.skill_ids)

            to_delete = current_skills - incoming_skills
            if to_delete:
                delete_user_skills(self.user, to_delete)

            to_add = incoming_skills - current_skills
            if to_add:
                bulk_add_user_skills(self.user, to_add)

        return UserSerializer(self.user).data

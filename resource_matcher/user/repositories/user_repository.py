from user.models import EnumRole, User, UserSkill

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def save_user(serializer):
    serializer.save()

def get_all_users():
    return User.objects.all()

def get_available_employees(start, end):
    return User.objects.filter(
        available_from__lte=start,
        available_to__gte=end,
        role=EnumRole.employee
    ).prefetch_related("skills")

def get_user_skills(user):
    return set(UserSkill.objects.filter(user=user).values_list("skill_id", flat=True))

def delete_user_skills(user, skill_ids):
    UserSkill.objects.filter(user=user, skill_id__in=skill_ids).delete()

def bulk_add_user_skills(user, skill_ids):
    UserSkill.objects.bulk_create([
        UserSkill(user=user, skill_id=skill_id) for skill_id in skill_ids
    ])

def update_user_availability(user, available_from, available_to):
    user.available_from = available_from
    user.available_to = available_to
    user.save()

def save_user_serializer(serializer):
    serializer.save()
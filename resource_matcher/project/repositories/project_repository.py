from project.models import Project

def get_project_by_id(project_id):
    try:
        return Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return None

def create_project(data):
    return Project.objects.create(**data)

def list_projects_by_creator(user):
    return Project.objects.filter(created_by=user)

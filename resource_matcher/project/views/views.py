from rest_framework.decorators import api_view
from project.services.project_service import create_project_service, list_project_service
from project.services.skill_service import list_skills_service
from project.services.task_service import create_task_service, list_tasks_service, match_resources_to_task_service
from resource_matcher.utils import user_login_required

@api_view(['POST'])
@user_login_required
def create_project(request):
    return create_project_service(request)

@api_view(['POST'])
@user_login_required
def create_task(request, project_id):
    return create_task_service(request, project_id)

@api_view(['GET'])
@user_login_required
def task_match_resources(request, task_id):
    return match_resources_to_task_service(request, task_id)

@api_view(['GET'])
@user_login_required
def list_skills(request):
    return list_skills_service()

@api_view(['GET'])
@user_login_required
def list_projects(request):
    return list_project_service(request)

@api_view(['GET'])
@user_login_required
def list_tasks(request):
    return list_tasks_service(request)
import logging
from rest_framework.response import Response
from rest_framework import status
from project.serializers.task_serializers import TaskSerializer
from resource_matcher.utils import Error
from ..repositories.task_repository import create_task, get_task_by_id, list_tasks_by_creator, list_all_tasks
from ..repositories.project_repository import get_project_by_id
from project.factories.task_factory import TaskFactory
from project.builders.task_match_builder import TaskMatchBuilder

logger = logging.getLogger(__name__)

def create_task_service(request, project_id):
    project = get_project_by_id(project_id)
    if not project:
        return Error("Project not found", status.HTTP_404_NOT_FOUND)

    if project.created_by != request.current_user:
        return Error("Only project creator can add tasks", status.HTTP_403_FORBIDDEN)

    data = request.data.copy()
    data['project'] = project.id # type: ignore
    serializer = TaskFactory.get_create_serializer(data)

    if serializer.is_valid():
        try:
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=201)
        except Exception as e:
            logger.exception("Error while creating task")
            return Error("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=400)


def list_tasks_service(request):
    if request.current_role == 'Manager':
        tasks = list_tasks_by_creator(request.current_user)
    else:
        tasks = list_all_tasks()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=200)

def match_resources_to_task_service(request, task_id):
    task = get_task_by_id(task_id)
    if not task:
        return Error("Task not found", status.HTTP_404_NOT_FOUND)

    required_skills = task.required_skill.values("id", "name")
    if not required_skills:
        return Error("Task has no required skills", status.HTTP_400_BAD_REQUEST)

    builder = TaskMatchBuilder(task)
    matched_users = builder.build()

    return Response({
        "task": {
            "id": task.id, # type: ignore
            "name": task.name,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "required_skills": list(required_skills),
        },
        "matched_users": matched_users
    })

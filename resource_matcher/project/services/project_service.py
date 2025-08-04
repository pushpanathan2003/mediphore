import logging
from rest_framework.response import Response
from rest_framework import status
from project.repositories.project_repository import create_project, list_projects_by_creator
from project.serializers.project_serializers import ProjectSerializer
from resource_matcher.utils import Error
from project.factories.project_factory import ProjectFactory

logger = logging.getLogger(__name__)

def create_project_service(request):
    if request.current_role != 'Manager':
        return Error("Only managers can create projects", status.HTTP_403_FORBIDDEN)

    data = request.data.copy()
    data['created_by'] = request.current_user.id

    serializer = ProjectFactory.get_serializer(data)
    if serializer.is_valid():
        try:
            create_project(serializer.validated_data)
            return Response(serializer.data, status=201)
        except Exception:
            logger.exception("Error while saving project")
            return Error("Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=400)

def list_project_service(request):
    projects = list_projects_by_creator(request.current_user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=200)
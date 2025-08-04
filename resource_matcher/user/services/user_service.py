import jwt
import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from user.builders.user_builder import UserAvailabilityBuilder
from user.factories.user_factory import UserFactory
from user.repositories.user_repository import get_all_users, get_user_by_email
from user.serializers.user_serializers import UserSerializer
from resource_matcher.utils import Error

from logging import getLogger

logger = getLogger(__name__)

def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Error("Email or Password cannot be blank.", status_code=status.HTTP_406_NOT_ACCEPTABLE)

        user = get_user_by_email(email)
        if user is None or not user.check_password(password):
            return Error("Invalid credentials.", status_code=status.HTTP_406_NOT_ACCEPTABLE)

        payload = {
            'id': user.id, # type: ignore
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.ADMIN_SESSION_EXPIRY_TIME),
            'iat': datetime.datetime.utcnow(),
            'role': user.role.value,
            'scope': 'user'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({
            'id': user.id, # type: ignore
            'access_token': token,
            'email': user.email,
            'name': user.name,
            'role': user.role.value
        })
    except Exception as e:
        logger.exception("Login failed")
        return Error("Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_user_details(request):
    serializer = UserSerializer(request.current_user)
    return Response(serializer.data)

def logout_user(request):
    return Response({"message": "Logged out"}, status=status.HTTP_204_NO_CONTENT)

def list_users(request):
    if request.current_role != 'Manager':
        return Error("Forbidden", status.HTTP_403_FORBIDDEN)
    users = get_all_users()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# def register_user(request):
#     serializer, errors = UserFactory.create_from_request(request.data)
#     if errors:
#         return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
def register_user(request):
    serializer, errors = UserFactory.create_from_request(request.data)

    if errors or serializer is None:
        return Response(errors or {"detail": "Unknown error"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def update_availability(request):
    try:
        user = request.current_user
        skill_ids = request.data.get("skills", [])
        available_from = request.data.get("available_from")
        available_to = request.data.get("available_to")

        if not isinstance(skill_ids, list):
            return Response({"error": "'skills' must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        if not available_from or not available_to:
            return Response({"error": "'available_from' and 'available_to' are required"}, status=status.HTTP_400_BAD_REQUEST)

        builder = UserAvailabilityBuilder(user)
        builder.set_availability_range(available_from, available_to).set_skills(skill_ids)
        serialized_data = builder.build()

        return Response(serialized_data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Availability update failed")
        return Error("Failed to update availability", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
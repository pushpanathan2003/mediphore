from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.serializers.user_serializers import UserSerializer
from user.services.user_service import get_user_details, list_users, register_user, update_availability
from resource_matcher.utils import user_login_required

@swagger_auto_schema(
    method='get',
    operation_description="Get logged-in user details",
    manual_parameters=[openapi.Parameter('HTTP_AUTHORIZATION', openapi.IN_HEADER, description="Bearer Token", type=openapi.TYPE_STRING)]
)
@api_view(['GET'])
@user_login_required
def user_detail_view(request, *args, **kwargs):
    return get_user_details(request)

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    operation_description="Register a new user",
    responses={201: UserSerializer()}
)
@api_view(['POST'])
def user_register_view(request):
    return register_user(request)

@swagger_auto_schema(
    method='get',
    operation_description="List all users (Manager only)",
    manual_parameters=[openapi.Parameter('HTTP_AUTHORIZATION', openapi.IN_HEADER, description="Bearer Token", type=openapi.TYPE_STRING)],
    responses={200: UserSerializer(many=True)}
)
@api_view(['GET'])
@user_login_required
def user_list_view(request):
    return list_users(request)

@swagger_auto_schema(
    method='put',
    operation_description="Add or update resource availability and skills",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'skills': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
            'available_from': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'available_to': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
        },
        required=['skills', 'available_from', 'available_to']
    ),
    responses={200: UserSerializer()}
)
@api_view(['PUT'])
@user_login_required
def add_or_update_availability(request):
    return update_availability(request)
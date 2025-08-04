from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from resource_matcher.utils import user_login_required
from user.services.user_service import login_user, logout_user

@swagger_auto_schema(
    method='post',
    operation_description="Login user and get JWT token",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email', 'password']
    ),
    responses={200: openapi.Response(description="JWT token")}
)
@api_view(['POST'])
def user_login_view(request):
    return login_user(request)

@swagger_auto_schema(
    method='delete',
    operation_description="Logout user",
    manual_parameters=[openapi.Parameter('HTTP_AUTHORIZATION', openapi.IN_HEADER, description="Bearer Token", type=openapi.TYPE_STRING)],
    responses={204: openapi.Response(description="Logged out")}
)
@api_view(['DELETE'])
@user_login_required
def user_logout_view(request, current_user, *args, **kwargs):
    return logout_user(request)


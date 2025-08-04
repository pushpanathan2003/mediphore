from rest_framework.response import Response
from rest_framework import status
from django.conf import settings as conf_settings
import jwt
from user.models import User
from functools import wraps

def Error(errors, status_code):
    if isinstance(errors, list):
        return Response({'errors': errors}, status=status_code)
    else:
        return Response({'errors': [errors]}, status=status_code)

def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):  
        
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith("Bearer "):
            return Error("Unauthorized!", status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ")[1]
        if not token:
            return Error("Unauthorized!", status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, conf_settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Error("Token expired", status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Error("Invalid token", status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=payload['id'])

        except User.DoesNotExist:
            return Error("User not found", status.HTTP_401_UNAUTHORIZED)

        # Inject user into request (acts like context)
        request.current_user = user
        request.current_role = user.role.value

        return view_func(request, *args, **kwargs)
    return wrapper

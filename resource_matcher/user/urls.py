from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from user.views.auth_views import user_login_view, user_logout_view
from user.views.user_views import add_or_update_availability, user_detail_view, user_list_view, user_register_view

urlpatterns = [
    path('auth/login', user_login_view, name='user_login'),
    path('auth/detail', user_detail_view, name='user_detail'),
    path('auth/logout', user_logout_view, name='user_logout'),
    path('auth/register', user_register_view, name='user_register'),
    path('auth/list', user_list_view, name='user_list'),
    path('users/me/skills-availability', add_or_update_availability, name='skills_availability'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

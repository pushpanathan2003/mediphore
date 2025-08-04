from django.urls import path

from project.views.views import create_project, create_task, list_projects, list_skills, list_tasks, task_match_resources

urlpatterns = [
    path('projects/create', create_project, name='create_project'),
    path('projects/<int:project_id>/tasks/create', create_task, name='create_task'),
    path('tasks/<int:task_id>/match', task_match_resources, name='task_match_resources'),
    path('skills', list_skills, name='list_skills'),
    path('projects', list_projects, name='list_projects'),
    path('tasks', list_tasks, name='list_tasks'),

]

from django.urls import path
from .views import welcome_tasks_app, TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('', welcome_tasks_app, name='welcome_tasks_app'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),

]

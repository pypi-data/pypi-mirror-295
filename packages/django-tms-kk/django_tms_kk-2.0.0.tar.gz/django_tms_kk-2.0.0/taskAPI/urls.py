from django.urls import path
from .views import get_tasks, task_detail, create_task

urlpatterns = [
    path('tasks',get_tasks),
    path('tasks/create',create_task),
    path('task/get/<int:pk>',task_detail),
    path('task/update/<int:pk>',task_detail),
    path('task/delete/<int:pk>',task_detail),
    
]

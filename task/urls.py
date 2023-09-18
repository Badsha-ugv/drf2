from django.urls import path
from .views import TaskListCreateView, TaskDetailView,index,task_detail,task_update

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('index/',index,name='index'),
    path('task-detail/<int:pk>/', task_detail),
    path('tasks/<int:pk>/update/', task_update, name='task-update'),


]

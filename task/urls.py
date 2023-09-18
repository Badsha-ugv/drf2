from django.urls import path
from .views import TaskListCreateView, TaskDetailView,index,task_detail,task_update, registration, user_login, login, logout_view

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('',index,name='index'),
    path('task-detail/<int:pk>/', task_detail),
    path('tasks/<int:pk>/update/', task_update, name='task-update'),

    path('registration/',registration,name='registration'),
    path('login/', user_login, name='user_login'),
    path('logout/', logout_view, name='user_logout'),
   


]

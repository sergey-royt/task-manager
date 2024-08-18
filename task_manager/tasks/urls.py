from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TaskIndexView.as_view(), name='task_index'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path(
        '<int:pk>/update/',
        views.TaskUpdateView.as_view(),
        name='task_update'
    ),
]

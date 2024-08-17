from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TaskIndexView.as_view(), name='task_index'),
]

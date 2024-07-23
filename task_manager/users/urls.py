from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UserIndexView.as_view(), name='users_index'),
]

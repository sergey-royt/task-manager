from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UserIndexView.as_view(), name='users_index'),
    path('create/', views.UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/',
         views.UserUpdateView.as_view(),
         name='users_update'),
    path('password/',
         views.ChangeUserPasswordView.as_view(),
         name='change_password'),
    path('<int:pk>/delete/',
         views.UserDeleteView.as_view(),
         name='users_delete')
]

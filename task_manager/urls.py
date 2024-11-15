from django.contrib import admin
from django.urls import path, include

from task_manager.views import IndexView, UserLoginView, UserLogoutView
from task_manager.settings import DEBUG


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("labels/", include("task_manager.labels.urls")),
]

if DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

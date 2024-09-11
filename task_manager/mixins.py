from typing import Callable

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    """Doesn't allow user make action if he is not logged in
    and redirect him to login page"""
    auth_message = _("You aren't authorised! Please log in.")

    def dispatch(
            self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect:
        if request.user.is_anonymous:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    """Doesn't allow user to change other user"""
    permission_denied_url: str | None = None

    def check_func(self) -> bool:
        return self.request.user == self.get_object()

    def get_test_func(self) -> Callable:
        return self.check_func

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class AuthorPermissionMixin(UserPermissionMixin):
    """Doesn't allow user to change objects created by other users"""
    def check_func(self) -> bool:
        return self.get_object().author == self.request.user

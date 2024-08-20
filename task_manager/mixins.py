from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    auth_message = _("You aren't authorised! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    permission_denied_url = None

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class DeleteProtectionMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class AuthorPermissionMixin(UserPermissionMixin):
    def test_func(self):
        return self.get_object().author == self.request.user

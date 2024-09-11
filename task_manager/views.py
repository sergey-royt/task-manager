from typing import Any, Coroutine

from django.db.models import ProtectedError
from django.http import (
    HttpResponseRedirect,
    HttpRequest,
    HttpResponseNotAllowed
)
from django.shortcuts import redirect
from django.views.generic import DeleteView
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class IndexView(TemplateView):
    """Main page view"""
    template_name = 'index.html'
    extra_context = {'title': _('Greetings from Hexlet!'),
                     'text': _('Practical programming courses'),
                     'button_text': _('Learn more')}


class UserLoginView(SuccessMessageMixin, LoginView):
    """Log in view with success message"""
    template_name = 'form.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('index')
    extra_context = {'title': _('Authorization'),
                     'button_text': _('Login')}

    success_message = _('You are Logged in')


class UserLogoutView(LogoutView):
    """Log out view"""
    next_page = reverse_lazy('index')

    def dispatch(
            self, request: HttpRequest, *args, **kwargs
    ) -> Coroutine[Any, Any, HttpResponseNotAllowed] | HttpResponseNotAllowed:

        messages.add_message(request, messages.INFO, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class ProtectedDeleteView(SuccessMessageMixin, DeleteView):
    """Delete view with protection and success messages"""
    protected_message: str | None = None
    protected_url: str | None = None

    def delete(
            self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect:

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, self.success_message)
        return HttpResponseRedirect(success_url)

    def post(
            self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect:

        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)

from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
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
    template_name = 'index.html'
    extra_context = {'title': _('Greetings from Hexlet!'),
                     'text': _('Practical programming courses'),
                     'button_text': _('Learn more')}


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('index')
    extra_context = {'title': _('Authorization'),
                     'button_text': _('Login')}

    success_message = _('You are Logged in')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class ProtectedDeleteView(SuccessMessageMixin, DeleteView):
    protected_message = None
    protected_url = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, self.success_message)
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)

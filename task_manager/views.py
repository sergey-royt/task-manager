from http import HTTPStatus

from django.shortcuts import render
from django.views.generic.base import TemplateView, View
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


class PageNotFoundView(View):
    template = '404.html'

    def get(self, request, *args, **kwargs):
        return render(
            request, template_name=self.template, status=HTTPStatus.NOT_FOUND
        )

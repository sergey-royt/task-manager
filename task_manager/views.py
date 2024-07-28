from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView, SuccessMessageMixin):
    template_name = 'form.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('index')
    extra_context = {'title': _('Authorization'),
                     'button_text': _('Login')}
    success_message = _('You are Logged in')

class UserLogoutView(LogoutView, ):
    next_page = reverse_lazy('index')

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from .forms import UserCreateForm
from django.urls import reverse_lazy


# Create your views here.
class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'form.html'
    success_message = _('User successfully created')
    success_url = reverse_lazy('login')
    extra_context = {'title': _('Registration'),
                     'button_text': _('Register ')}

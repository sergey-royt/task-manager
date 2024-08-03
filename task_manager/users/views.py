from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from .forms import UserForm
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin


# Create your views here.
class UserIndexView(ListView):
    model = CustomUser
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['pk']


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'form.html'
    success_message = _('User successfully created')
    success_url = reverse_lazy('login')
    extra_context = {'title': _('Registration'),
                     'button_text': _('Register')}


class UserUpdateView(AuthRequiredMixin, UserPermissionMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = CustomUser
    form_class = UserForm
    template_name = 'form.html'
    success_message = _('User successfully updated')
    success_url = reverse_lazy('users_index')
    extra_context = {'title': _('Updating users'),
                     'button_text': _('Update')}

    permission_denied_url = reverse_lazy('users_index')
    permission_denied_message = _("You don't have rights to update other users.")

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from .forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView


User = get_user_model()


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['pk']


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'form.html'
    success_message = _('User successfully created')
    success_url = reverse_lazy('login')
    extra_context = {'title': _('Registration'),
                     'button_text': _('Register')}


class UserUpdateView(AuthRequiredMixin,
                     UserPermissionMixin,
                     SuccessMessageMixin,
                     UpdateView):

    permission_denied_url = reverse_lazy('users_index')
    login_url = reverse_lazy('login')
    model = User
    form_class = UserUpdateForm
    template_name = 'form.html'
    success_message = _('User successfully updated')
    permission_denied_message = _(
        "You don't have rights to update other users."
    )
    success_url = reverse_lazy('users_index')
    extra_context = {'title': _('Updating user'),
                     'button_text': _('Update')}


class ChangeUserPasswordView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    PasswordChangeView
):
    login_url = reverse_lazy('login')
    form_class = PasswordChangeForm
    success_message = _('The password has been successfully updated')
    permission_denied_url = reverse_lazy('users_index')
    template_name = 'users/change_password.html'
    extra_context = {'button_text': _('Change password')}

    def get_success_url(self):
        return reverse_lazy('users_update', kwargs={'pk': self.request.user.pk})


class UserDeleteView(AuthRequiredMixin,
                     UserPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):

    login_url = reverse_lazy('login')
    success_message = _('User successfully deleted')
    success_url = reverse_lazy('users_index')
    template_name = 'users/delete.html'
    model = User
    extra_context = {'title': _('Deleting user'),
                     'text': _('Are you sure you want to delete'),
                     'button_text': _('Yes, delete')}

    permission_denied_url = reverse_lazy('users_index')
    permission_denied_message = _(
        "You don't have rights to delete other users."
    )

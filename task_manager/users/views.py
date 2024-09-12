from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from .forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin
from django.contrib.auth import get_user_model

from task_manager.views import ProtectedDeleteView

User = get_user_model()


class UserIndexView(ListView):
    """Render list of user objects"""

    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['pk']


class UserCreateView(SuccessMessageMixin, CreateView):
    """User object create view with success message"""

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
    """User object update view with permission check
    and success and permission denied messages"""

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


class UserDeleteView(AuthRequiredMixin,
                     UserPermissionMixin,
                     ProtectedDeleteView):
    """
    User object delete view with delete protection
    if user have tasks. Has a permission check and
    result messages
    """

    protected_message = _('It is not possible to delete a user '
                          'because it is being used')
    protected_url = reverse_lazy('users_index')
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
        "You don't have rights to update other users."
    )

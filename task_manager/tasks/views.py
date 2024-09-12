from typing import Any

from django.views.generic import DetailView
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, AuthorPermissionMixin
from .filters import TaskFilter
from .models import Task
from .forms import TaskForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskIndexView(AuthRequiredMixin, FilterView):
    """Render list of Task objects ordered by pk and filter form"""

    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }
    ordering = ['pk']


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Task object create view with success message
    and authentication check"""

    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_index')
    success_message = _('The task has been successfully created')
    extra_context = {
        'title': _('Create task'),
        'button_text': _('Create'),
    }

    def form_valid(self, form: TaskForm) -> Any:
        """add User object pk reference
        to Task object author attribute"""

        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin,
                     UpdateView
                     ):
    """Task object update view with permission check
    and success message"""

    model = Task
    form_class = TaskForm
    success_message = _('The task has been successfully updated')
    success_url = reverse_lazy('task_index')
    template_name = 'form.html'
    extra_context = {
        'title': _('Updating task'),
        'button_text': _('Update'),
    }


class TaskDeleteView(AuthRequiredMixin,
                     AuthorPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    """Task object delete view.
    Only Task author can delete it.
    Add success or permission denied messages to response"""

    success_message = _('The task has been successfully deleted')
    success_url = reverse_lazy('task_index')
    template_name = 'tasks/delete.html'
    model = Task
    extra_context = {'title': _('Deleting task'),
                     'text': _('Are you sure you want to delete'),
                     'button_text': _('Yes, delete')}

    permission_denied_url = reverse_lazy('task_index')
    permission_denied_message = _(
        "Only the author of the task can delete it"
    )


class TaskDetailView(AuthRequiredMixin, DetailView):
    """Task object detail view
    authorization required"""

    template_name = 'tasks/details.html'
    model = Task
    extra_context = {'title': _('Task details')}

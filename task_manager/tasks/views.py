from django_filters.views import FilterView
from task_manager.mixins import AuthRequiredMixin
from .filters import TaskFilter
from .models import Task
from django.utils.translation import gettext_lazy as _


class TaskIndexView(AuthRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }
    ordering = ['pk']

from typing import Any

from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from .models import Task
from task_manager.labels.models import Label
from django import forms
from django.utils.translation import gettext_lazy as _


class TaskFilter(FilterSet):
    """Filter for Task objects
    filter by status, labels, executor
    Has checkbox to show only user's own tasks"""

    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_("Label"))

    own_tasks = BooleanFilter(
        label=_("Only own tasks"),
        widget=forms.CheckboxInput,
        method="get_own_tasks",
    )

    def get_own_tasks(self, queryset: Any, name: Any, value: Any) -> Any:
        """filter queryset if checkbox is marked
        left only user's own tasks"""

        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

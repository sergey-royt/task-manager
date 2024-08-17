from django_filters import FilterSet, BooleanFilter
from .models import Task
from django import forms
from django.utils.translation import gettext_lazy as _


class TaskFilter(FilterSet):
    own_tasks = BooleanFilter(
        label=_('Only own tasks'),
        widget=forms.CheckboxInput,
        method='get_own_tasks',
    )

    def get_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']

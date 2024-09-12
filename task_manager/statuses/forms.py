from django.forms import ModelForm
from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    """Status form contains only name field"""

    class Meta:
        model = Status
        fields = ['name']

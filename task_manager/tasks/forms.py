from django.forms import ModelForm
from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    """Task create form with
    name, description, status, executor, labels fields"""

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]

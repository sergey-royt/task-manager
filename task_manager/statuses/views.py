from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from task_manager.statuses.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from .forms import StatusForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin
from task_manager.views import ProtectedDeleteView


class StatusIndexView(AuthRequiredMixin, ListView):
    """Render list of Status object ordered by pk"""

    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"
    ordering = ["pk"]


class StatusCreateView(
    SuccessMessageMixin,
    AuthRequiredMixin,
    CreateView,
):
    """Status object create view with success message
    and authentication check"""

    form_class = StatusForm
    template_name = "form.html"
    login_url = reverse_lazy("login")
    success_message = _("The status has been successfully created")
    success_url = reverse_lazy("status_index")
    extra_context = {"title": _("Create status"), "button_text": _("Create")}


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Task object update view with authentication check
    and success message"""

    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_message = _("The status has been successfully updated")
    success_url = reverse_lazy("status_index")
    extra_context = {"title": _("Updating status"), "button_text": _("Update")}


class StatusDeleteView(AuthRequiredMixin, ProtectedDeleteView):
    """Status object delete view with delete protection
    if status is bound to any task.
    Has an authentication check and result messages"""

    login_url = reverse_lazy("login")
    success_message = _("The status has been successfully deleted")
    success_url = reverse_lazy("status_index")
    template_name = "statuses/delete.html"
    model = Status
    extra_context = {
        "title": _("Deleting status"),
        "text": _("Are you sure you want to delete"),
        "button_text": _("Yes, delete"),
    }
    protected_url = reverse_lazy("status_index")
    protected_message = _("Cannot delete status because it in use")

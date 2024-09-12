from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin
from .forms import LabelForm
from task_manager.views import ProtectedDeleteView


class LabelIndexView(AuthRequiredMixin, ListView):
    """Render list of Labels ordered by pk"""

    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['pk']


class LabelCreateView(SuccessMessageMixin, AuthRequiredMixin, CreateView):
    """Label object create view with success message
    and authentication check"""

    form_class = LabelForm
    template_name = 'form.html'
    success_message = _('The label has been successfully created')
    success_url = reverse_lazy('labels_index')
    extra_context = {'title': _('Create label'),
                     'button_text': _('Create')}


class LabelUpdateView(SuccessMessageMixin, AuthRequiredMixin, UpdateView):
    """Label object update view with authentication check
    and success message"""

    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_message = _('The label has been successfully updated')
    success_url = reverse_lazy('labels_index')
    extra_context = {'title': _('Updating label'),
                     'button_text': _('Update')}


class LabelDeleteView(AuthRequiredMixin,
                      ProtectedDeleteView):
    """
    Label object delete view with delete protection
    if user have tasks. Has a authentication check and
    result messages
    """

    success_message = _('The label has been successfully deleted')
    success_url = reverse_lazy('labels_index')
    template_name = 'labels/delete.html'
    model = Label
    extra_context = {'title': _('Deleting label'),
                     'text': _('Are you sure you want to delete'),
                     'button_text': _('Yes, delete')}
    protected_url = reverse_lazy('labels_index')
    protected_message = _('Cannot delete label because it in use')

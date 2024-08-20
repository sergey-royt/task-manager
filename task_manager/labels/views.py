from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin
from .forms import LabelForm


class LabelIndexView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['pk']


class LabelCreateView(SuccessMessageMixin, AuthRequiredMixin, CreateView):
    form_class = LabelForm
    template_name = 'form.html'
    success_message = _('The label has been successfully created')
    success_url = reverse_lazy('labels_index')
    extra_context = {'title': _('Create label'),
                     'button_text': _('Create')}

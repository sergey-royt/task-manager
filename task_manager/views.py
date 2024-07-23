from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.translation import gettext


class IndexView(TemplateView):
    template_name = 'index.html'

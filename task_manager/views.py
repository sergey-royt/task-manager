from django.shortcuts import render
from django.views.generic.base import View
from django.utils.translation import gettext


class IndexView(View):
    title = gettext('Task manager Hexlet')

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {'title': self.title})

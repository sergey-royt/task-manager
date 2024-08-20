from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):
    class Meta(ModelForm):
        model = Label
        fields = ['name']

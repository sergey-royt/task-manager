from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):
    """Label form contains only name field"""

    class Meta(ModelForm):
        model = Label
        fields = ["name"]

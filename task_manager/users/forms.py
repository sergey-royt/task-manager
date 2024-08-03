from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']



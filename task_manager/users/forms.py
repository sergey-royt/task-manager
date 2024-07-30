from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _


MIN_USERNAME_LENGTH = 5
MAX_USERNAME_LENGTH = 20
MAX_NAME_LENGTH = 30


class UserForm(UserCreationForm):
    username = forms.CharField(
        min_length=MIN_USERNAME_LENGTH,
        max_length=MAX_USERNAME_LENGTH,
        help_text=_('Not shorter than 5 chars. Not longer than 20 chars.'),
        label=_('Username')
    )
    first_name = forms.CharField(
        max_length=MAX_NAME_LENGTH,
        required=False,
        help_text=_('Not longer than 30 chars.'),
        label=_('First name')
    )
    last_name = forms.CharField(
        max_length=MAX_NAME_LENGTH,
        required=False,
        help_text=_('Not longer than 30 chars.'),
        label=_('Last name')
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name')
        }




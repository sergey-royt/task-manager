from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]


class UserUpdateForm(UserChangeForm):
    password = forms.CharField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "password, but you can change it using "
            '<a href="{}">this form</a>.'
        ),
        initial="****************",
        disabled=True
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        password = self.fields.get('password')
        password.help_text = password.help_text.format(
            reverse_lazy("change_password")
        )

    def clean_username(self):
        if (
                self.get_initial_for_field(
                    self.fields['username'], 'username'
                ).lower()
                !=
                self.cleaned_data.get('username').lower()
        ):
            return self._clean_username()
        else:
            return self.cleaned_data.get("username")

    def _clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            username
            and
                self._meta.model.objects.filter(
                    username__iexact=username
                ).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username

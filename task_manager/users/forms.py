from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]


class UserUpdateForm(UserCreateForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

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

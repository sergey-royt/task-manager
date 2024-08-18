from django.core.exceptions import ValidationError

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        new_username = self.cleaned_data.get("username")
        old_username = self.get_initial_for_field(
            self.fields['username'], 'username'
        )

        if new_username.lower() != old_username.lower():
            if (
                    new_username
                    and
                    self._meta.model.objects.filter(
                        username__iexact=new_username
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
                return new_username
        else:
            return new_username

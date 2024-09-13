from typing import Any

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateForm(UserCreationForm):
    """User create form with
    first_name, last_name, username, password1 and password2 fields"""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]


class UserUpdateForm(UserCreateForm):
    """User update form inherits from UserCreateForm
    add ability to not update username or only change letter case"""

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_username(self) -> Any | None:
        """is_username_change return False if only letter case changed"""
        is_username_changed = (
            self.get_initial_for_field(
                self.fields["username"], "username"
            ).lower()
            != self.cleaned_data.get("username").lower()
        )

        if is_username_changed:
            return super().clean_username()
        else:
            return self.cleaned_data.get("username")

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
        username = self.cleaned_data.get("username")
        return username

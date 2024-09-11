from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from .settings import MIN_PASSWORD_LENGTH, USERNAME_MAX_LENGTH


class CustomUser(AbstractUser):
    """Custom User Model overwriting base user model
    with flexible max_length for first_name
    and last_name, and min password length
    (can be set up using env variables specified in users/settings.py)
    Has an overwritten __str__ method returning full name"""
    first_name = models.CharField(
        _("first name"), max_length=USERNAME_MAX_LENGTH
    )
    last_name = models.CharField(
        _("last name"), max_length=USERNAME_MAX_LENGTH
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[MinLengthValidator(MIN_PASSWORD_LENGTH)])

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def __str__(self) -> str:
        """
        :return: string f'{first_name} {last_name}'
        """
        return self.get_full_name()

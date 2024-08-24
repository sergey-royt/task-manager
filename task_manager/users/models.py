from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


NAME_MAX_LENGTH = 30
MIN_PASSWORD_LENGTH = 8


class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(_("last name"), max_length=NAME_MAX_LENGTH)
    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[MinLengthValidator(MIN_PASSWORD_LENGTH)])

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def __str__(self):
        return self.get_full_name()

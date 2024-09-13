from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Status model with fields:
    :name: CharField,
    :created_at: DateTimeField"""

    name = models.CharField(
        max_length=150, unique=True, blank=False, verbose_name=_("Name")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date of creation")
    )

    def __str__(self) -> models.CharField:
        """Return status name"""

        return self.name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")

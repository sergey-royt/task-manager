from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """
    Label model with fields:
    :name: CharField
    :created_at: DateTimeFiled
    """

    name = models.CharField(max_length=150,
                            unique=True,
                            blank=False,
                            verbose_name=_('Name'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creation')
    )

    def __str__(self) -> models.CharField:
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

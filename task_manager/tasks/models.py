from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name=_('Name')
    )

    description = models.TextField(
        blank=False,
        verbose_name=_('Description'),
        max_length=5000
        )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creation')
    )

    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
        related_name='author'
    )

    status = models.ForeignKey(
        Status,
        verbose_name=_('Status'),
        on_delete=models.PROTECT,
        related_name='status'
    )
    executor = models.ForeignKey(
        User,
        verbose_name=_('Executor'),
        related_name='executor',
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

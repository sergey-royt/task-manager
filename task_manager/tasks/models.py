from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_('Name')
    )

    description = models.TextField(
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
        blank=True,
        null=True
    )

    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        blank=True,
        related_name='labels',
        verbose_name=_('Labels')
    )

    def __str__(self) -> models.CharField:
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

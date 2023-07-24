from django.db import models
from task_manager.user.models import User
from task_manager.status.models import Status
from task_manager.label.models import Label
from django.utils.translation import gettext as _


class Task(models.Model):

    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('status'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('author'),
    )
    executor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('executor'),
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        through='Labeled',
        verbose_name=_('labels'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Labeled(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

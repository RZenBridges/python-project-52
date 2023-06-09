from django.db import models
from task_manager.user.models import User
from task_manager.status.models import Status
from task_manager.label.models import Label


class Task(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name="task_status")
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="task_author")
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name="task_executor")
    labels = models.ManyToManyField(Label, through='Labeled')
    created_at = models.DateTimeField(auto_now_add=True)


class Labeled(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

from django.db import models
from task_manager.user.models import User
from task_manager.status.models import Status
from task_manager.label.models import Label


class Task(models.Model):

    name = models.CharField(max_length=100)
    body = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name="task_status")
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="task_author")
    performer = models.ForeignKey(User, on_delete=models.PROTECT,
                                  related_name="task_performer")
    labels = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from task_manager.user.models import User


class Task(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="task_author")
    performer = models.ForeignKey(User, on_delete=models.PROTECT,
                                  related_name="task_performer")
    created_at = models.DateTimeField(auto_now_add=True)

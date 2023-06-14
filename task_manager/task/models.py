from django.db import models
from task_manager.user.models import User


class Task(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    performer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

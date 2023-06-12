from django.db import models
# from django.contrib.auth.models import AbstractUser


class User(models.Model):
    # email = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

#    USERNMAE_FIELD = "username"

#    def __str__(self):
#        return self.username

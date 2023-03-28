from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class User(AbstractUser):
    auth_token = models.CharField(max_length=50, blank=True, default='')
    email_varified=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.auth_token:
            self.auth_token = get_random_string(length=20)
        return super(User, self).save(*args, **kwargs)

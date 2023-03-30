from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField('email', max_length=40, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

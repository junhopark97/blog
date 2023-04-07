from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    class GenderStatus(models.TextChoices):
        FEMALE = 'F'
        MALE = 'M'
    first_name = None
    last_name = None

    email = models.EmailField('email', max_length=40, unique=True)
    username = models.CharField(max_length=20, unique=False)
    gender = models.CharField(
        choices=GenderStatus.choices, default=GenderStatus.MALE, max_length=1
    )
    # gender = models.CharField(max_length=1, choices=(('F', 'female'), ('M', 'male')), default='M')
    phone_number = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import AccountManager

# Create your models here.


class Account(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = AccountManager()

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_vendor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
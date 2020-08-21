from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager
from njiani.services.models import Service

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Mechanic(models.Model):
    location = models.CharField(max_length=100)
    rating = models.FloatField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    services = models.ManyToManyField(
        Service
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

class Customer(models.Model):
    location = models.CharField(max_length=100)
    rating = models.FloatField(blank=True, null=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )



from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
)
from django.contrib.auth.models import BaseUserManager

from .managers import UserManager
from role.models import Role
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    email = models.EmailField(
        max_length=100, unique=True, null=True, blank=True)
    role = models.ForeignKey(
        to=Role, on_delete=models.CASCADE, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["role","first_name","last_name"]

    class Meta:
        ordering = ['created_at']
        verbose_name = 'custom_user'
        verbose_name_plural = 'custom_users'
        db_table = 'custom_user'

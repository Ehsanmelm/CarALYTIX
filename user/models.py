from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
)
from django.contrib.auth.models import BaseUserManager

from .managers import UserManager
from role.models import Role
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, role, password, **extra_fields)


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
    REQUIRED_FIELDS = ["role"]

    class Meta:
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

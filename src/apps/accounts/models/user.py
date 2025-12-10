from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.core.managers import AccountManager
from apps.core.models import BaseModel
from apps.core.services.model_status import LanguageType, UserType


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ForeignKey('uploads.File', on_delete=models.SET_NULL, blank=True, null=True)

    role = models.CharField(max_length=20, choices=UserType.choices, default=UserType.ADMIN)
    language = models.CharField(max_length=20, choices=LanguageType.choices, default=LanguageType.EN)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def user_groups(self):
        return ", ".join([group.name for group in self.groups.all()])
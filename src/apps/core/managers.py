from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):

    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def only_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).dead()

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class AccountManager(DjangoUserManager, SoftDeleteManager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()
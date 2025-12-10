from django.db import models

from apps.core.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
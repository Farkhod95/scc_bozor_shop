from django.db import models

from apps.core.models import BaseModel


class Subcategory(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    photo = models.ForeignKey('uploads.File', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

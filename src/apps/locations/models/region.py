from django.db import models

from apps.core.models import BaseModel

class Region(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
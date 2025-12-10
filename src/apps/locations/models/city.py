from django.db import models

from apps.core.models import BaseModel

class City(BaseModel):
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
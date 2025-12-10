from django.db import models

from apps.core.models import BaseModel


class Bazar(BaseModel):
    name = models.CharField(max_length=255, null=True)
    city = models.ForeignKey('locations.City', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    total_places = models.IntegerField(default=0)

    def __str__(self):
        return self.name
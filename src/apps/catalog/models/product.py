from django.db import models

from apps.core.models import BaseModel
from apps.core.services.model_status import UnitType


class Product(BaseModel):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, choices=UnitType.choices, default=UnitType.KILOGRAM)

    def __str__(self):
        return self.name
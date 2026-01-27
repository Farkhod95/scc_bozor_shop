from django.db import models

from apps.core.models import BaseModel


class Place(BaseModel):
    slug = models.SlugField(unique=True, null=True)
    bazar = models.ForeignKey('Bazar', on_delete=models.CASCADE)
    section = models.ForeignKey('BazarSection', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.slug}"


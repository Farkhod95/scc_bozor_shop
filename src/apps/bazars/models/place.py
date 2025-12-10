from django.db import models

from apps.core.models import BaseModel


class Place(BaseModel):
    bazar = models.ForeignKey('Bazar', on_delete=models.CASCADE)
    number = models.IntegerField()
    qr_code = models.OneToOneField('QRCode', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.number}"


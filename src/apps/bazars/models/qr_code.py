from django.db import models

from apps.core.models import BaseModel


class QRCode(BaseModel):
    place = models.OneToOneField('Place', on_delete=models.CASCADE)
    qr_text = models.CharField(max_length=255)
    generate_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.qr_text
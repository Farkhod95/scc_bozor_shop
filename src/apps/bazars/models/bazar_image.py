from django.db import models

from apps.core.models import BaseModel


class BazarImage(BaseModel):
    bazar = models.ForeignKey(
        "Bazar",
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ForeignKey("uploads.File", on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image of {self.bazar.name}"

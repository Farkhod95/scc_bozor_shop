from django.db import models

from apps.core.models import BaseModel


class BazarSection(BaseModel):
    bazar = models.ForeignKey("Bazar", on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=255, null=False)
    svg = models.ForeignKey("uploads.File", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
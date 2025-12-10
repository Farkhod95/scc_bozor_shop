from django.db import models
from apps.core.models import BaseModel


class File(BaseModel):
    file = models.FileField(upload_to="files")

    def __str__(self):
        return f"{self.file}"

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ["-id"]
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from apps.core.models import BaseModel


class BazarReview(BaseModel):
    bazar = models.ForeignKey(
        'Bazar',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('bazar', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.bazar} ({self.rating})"
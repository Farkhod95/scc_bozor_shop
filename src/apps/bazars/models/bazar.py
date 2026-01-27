from django.db import models
from django.db.models import Avg, Count

from apps.core.models import BaseModel


class Bazar(BaseModel):
    name = models.CharField(max_length=255, null=True)
    managers = models.ManyToManyField("accounts.User")
    city = models.ForeignKey('locations.City', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    total_places = models.IntegerField(default=0)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    average_rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def recalculate_rating(self):
        stats = self.reviews.aggregate(avg=Avg('rating'), count=Count('id'))

        self.average_rating = stats['avg'] or 0.0
        self.review_count = stats['count'] or 0
        self.save()
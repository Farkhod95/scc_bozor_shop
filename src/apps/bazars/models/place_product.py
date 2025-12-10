from django.db import models

from apps.core.models import BaseModel


class PlaceProduct(BaseModel):
    place = models.ForeignKey("Place", on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} at {self.place.number}"
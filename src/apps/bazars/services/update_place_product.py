from decimal import Decimal
from typing import Dict, Any
from rest_framework.exceptions import NotFound, ValidationError

from apps.bazars.models import PlaceProduct, PlacePriceHistory


def update_place_product(
    *,
    place_product_id: int,
    price: Decimal | None = None,
    quantity: int | None = None,
    updated_by=None
) -> Dict[str, Any]:

    try:
        pp = PlaceProduct.objects.select_related('product', 'place').get(id=place_product_id)
    except PlaceProduct.DoesNotExist:
        raise NotFound({"message_key": "place_product_not_found"})

    if price is not None and pp.price != price:
        PlacePriceHistory.objects.create(
            place=pp.place,
            product=pp.product,
            price=pp.price,
            created_by=updated_by
        )
        pp.price = price

    if quantity is not None:
        pp.quantity = quantity

    pp.updated_by = updated_by
    pp.save()

    return {
        "id": pp.id,
        "place": pp.place_id,
        "product": pp.product_id,
        "price": str(pp.price),
        "quantity": pp.quantity
    }

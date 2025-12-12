from decimal import Decimal
from typing import Dict, Any
from rest_framework.exceptions import ValidationError, NotFound

from apps.catalog.models import Product
from apps.bazars.models import Place, PlaceProduct


def create_place_product(
    *,
    place_id: int,
    product_id: int,
    price: Decimal,
    quantity: int,
    created_by=None
) -> Dict[str, Any]:

    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise NotFound({"message_key": "place_not_found"})

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise NotFound({"message_key": "product_not_found"})

    if PlaceProduct.objects.filter(place=place, product=product).exists():
        raise ValidationError({"message_key": "product_already_exists_in_place"})

    obj = PlaceProduct.objects.create(
        place=place,
        product=product,
        price=price,
        quantity=quantity,
        created_by=created_by,
    )

    return {
        "id": obj.id,
        "place": obj.place_id,
        "product": obj.product_id,
        "price": str(obj.price),
        "quantity": obj.quantity,
    }

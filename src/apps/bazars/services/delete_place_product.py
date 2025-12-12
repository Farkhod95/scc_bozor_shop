from rest_framework.exceptions import NotFound
from apps.bazars.models import PlaceProduct


def delete_place_product(place_product_id: int):
    try:
        pp = PlaceProduct.objects.get(id=place_product_id)
    except PlaceProduct.DoesNotExist:
        raise NotFound({"message_key": "place_product_not_found"})

    pp.delete()

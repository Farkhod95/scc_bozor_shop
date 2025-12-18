from rest_framework.exceptions import NotFound
from apps.bazars.models import PlaceProduct
from apps.core.services.validate_bazar_admin import validate_bazar_admin


def delete_place_product(user, place_product_id: int):
    try:
        pp = PlaceProduct.objects.get(id=place_product_id)
    except PlaceProduct.DoesNotExist:
        raise NotFound({"message_key": "place_product_not_found"})

    validate_bazar_admin(user, pp.place.bazar_id)

    pp.delete()
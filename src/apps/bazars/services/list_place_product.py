from typing import List, Dict, Any
from apps.bazars.models import PlaceProduct
from apps.core.utils.translations import translate_response


def list_place_product(user, lang: str, bazar_id: int | None = None,) -> List[Dict[str, Any]]:
    queryset = PlaceProduct.objects.select_related('place', 'product')

    if bazar_id is not None:
        queryset = queryset.filter(place__bazar_id=bazar_id)

    data = []
    for pp in queryset:
        data.append({
            "id": pp.id,
            "place_id": pp.place.id,
            "place_number": pp.place.number,
            "product_id": pp.product.id,
            "product_name": (
                translate_response(
                    obj=pp.product,
                    fields=["name"],
                    lang=lang,
                    is_admin=False
                )["name"]
            ),
            "product_unit": pp.product.unit,
            "price": str(pp.price),
            "quantity": pp.quantity
        })

    return data

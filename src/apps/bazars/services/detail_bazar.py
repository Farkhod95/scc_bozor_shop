from rest_framework.exceptions import NotFound

from apps.bazars.models import Bazar
from apps.core.utils.translations import translate_response


def get_bazar_detail(*, bazar_id: int, user, lang: str) -> dict:
    try:
        obj = Bazar.objects.select_related("city", "city__region").get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise NotFound({"message_key": "category_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["name"],
        lang=lang,
        is_admin=is_admin
    )

    data.update({
        "city_id": obj.city.id,
        "city": obj.city.name,
        "region": obj.city.region.name,
        "total_places": obj.total_places,
        "created_at": obj.created_at
    })

    return data

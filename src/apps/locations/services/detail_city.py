from rest_framework.exceptions import NotFound
from apps.locations.models import City
from apps.core.utils.translations import translate_response


def get_city_detail(*, city_id: int, user, lang: str) -> dict:
    try:
        obj = City.objects.get(id=city_id)
    except City.DoesNotExist:
        raise NotFound({"message_key": "city_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["name"],
        lang=lang,
        is_admin=is_admin
    )

    data.update({
        "id": obj.id,
        "region_id": obj.region_id,
        "code": obj.code,
        "region_name": (
            translate_response(
                obj=obj.region,
                fields=["name"],
                lang=lang,
                is_admin=is_admin
            )["name"]
        ),
        "created_at": obj.created_at,
    })

    return data

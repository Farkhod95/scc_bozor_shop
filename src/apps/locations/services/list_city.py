from typing import Iterable, Dict, Any
from apps.locations.models import City
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import translate_response


def list_city(user, lang: str, filters=None, search=None) -> Iterable[Dict[str, Any]]:
    cities = City.objects.select_related("region").all().order_by("-id")
    is_admin = user.is_staff
    result = []

    search_fields = ["name", "code"]
    queryset = apply_filters_and_search(cities, filters=filters, search=search, search_fields=search_fields)

    for obj in queryset:
        city_data = translate_response(
            obj=obj,
            fields=["name"],
            lang=lang,
            is_admin=is_admin
        )

        city_data.update({
            "id": obj.id,
            "region_id": obj.region.id,
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

        result.append(city_data)

    return result

from typing import Iterable, Dict, Any
from apps.locations.models import Region
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import translate_response, expand_translated_fields


def list_region(user, lang: str, filters=None, search=None) -> Iterable[Dict[str, Any]]:
    regions = Region.objects.all().order_by("-id")
    is_admin = user.is_staff
    result = []

    search_fields = ["name", "code"]
    search_fields = expand_translated_fields(Region, search_fields)

    queryset = apply_filters_and_search(regions, filters=filters, search=search, search_fields=search_fields)


    for obj in queryset:
        region_data = translate_response(
            obj=obj,
            fields=["name"],
            lang=lang,
            is_admin=is_admin
        )

        region_data.update({
            "id": obj.id,
            "created_at": obj.created_at,
        })

        result.append(region_data)

    return result

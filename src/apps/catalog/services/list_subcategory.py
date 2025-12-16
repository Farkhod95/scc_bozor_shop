from typing import Iterable, Dict, Any
from apps.catalog.models import Subcategory
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import translate_response, expand_translated_fields


def list_subcategory(user, lang: str, filters=None, search=None) -> Iterable[Dict[str, Any]]:
    subcategories = Subcategory.objects.select_related("photo").all().order_by("-id")
    is_admin = user.is_staff
    result = []

    search_fields = ["title", "description"]
    search_fields = expand_translated_fields(Subcategory, search_fields)

    queryset = apply_filters_and_search(subcategories, filters=filters, search=search, search_fields=search_fields)

    for obj in queryset:
        subcategory_data = translate_response(
            obj=obj,
            fields=["title", "description"],
            lang=lang,
            is_admin=is_admin
        )

        subcategory_data.update({
            "id": obj.id,
            "created_at": obj.created_at,
            "photo": obj.photo.file.url if obj.photo else None,
        })

        result.append(subcategory_data)

    return result

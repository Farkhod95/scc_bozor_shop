from typing import Iterable, Dict, Any
from apps.catalog.models import Category
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import translate_response


def list_categories(user, lang: str, filters=None, search=None) -> Iterable[Dict[str, Any]]:
    categories = Category.objects.all().order_by("-id")
    is_admin = user.is_staff
    result = []

    search_fields = ["name", "address", "total_places", "city__name", "city__region__name"]
    queryset = apply_filters_and_search(categories, filters=filters, search=search, search_fields=search_fields)

    for obj in queryset:
        category_data = translate_response(
            obj=obj,
            fields=["title", "description"],
            lang=lang,
            is_admin=is_admin
        )

        category_data.update({
            "id": obj.id,
            "created_at": obj.created_at,
        })

        result.append(category_data)

    return result

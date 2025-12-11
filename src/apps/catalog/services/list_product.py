from typing import Iterable, Dict, Any
from apps.catalog.models import Product
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import translate_response


def list_products(user, lang: str, filters=None, search=None) -> Iterable[Dict[str, Any]]:
    products = Product.objects.select_related("category").all().order_by("-id")
    is_admin = user.is_staff
    result = []

    search_fields = ["name", "address", "total_places", "city__name", "city__region__name"]
    queryset = apply_filters_and_search(products, filters=filters, search=search, search_fields=search_fields)


    for obj in queryset:
        product_data = translate_response(
            obj=obj,
            fields=["name"],
            lang=lang,
            is_admin=is_admin
        )

        product_data.update({
            "id": obj.id,
            "unit": obj.unit,
            "category_id": obj.category.id,
            "category_name": (
                translate_response(
                    obj=obj.category,
                    fields=["title"],
                    lang=lang,
                    is_admin=is_admin
                )["title"]
            ),
            "created_at": obj.created_at,
        })

        result.append(product_data)

    return result

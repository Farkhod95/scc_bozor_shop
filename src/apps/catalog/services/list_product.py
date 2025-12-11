from typing import Iterable, Dict, Any
from apps.catalog.models import Product
from apps.core.utils.translations import translate_response


def list_products(user, lang: str) -> Iterable[Dict[str, Any]]:
    products = Product.objects.select_related("category").all().order_by("-id")
    is_admin = user.is_staff
    result = []

    for obj in products:
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

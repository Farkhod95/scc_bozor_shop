from typing import Dict, Any
from rest_framework.exceptions import NotFound
from apps.catalog.models import Product
from apps.core.utils.translations import translate_response


def get_product_detail(*, product_id: int, user, lang: str) -> Dict[str, Any]:
    try:
        obj = Product.objects.select_related("category", "subcategory").get(id=product_id)
    except Product.DoesNotExist:
        raise NotFound({"message_key": "product_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["name"],
        lang=lang,
        is_admin=is_admin
    )

    data.update({
        "id": obj.id,
        "category_id": obj.category_id,
        "category_name": (
            translate_response(
                obj=obj.category,
                fields=["title"],
                lang=lang,
                is_admin=is_admin
            )["title"]
        ),
        "subcategory_id": obj.subcategory_id,
        "subcategory_name": (
            translate_response(
                obj=obj.subcategory,
                fields=["title"],
                lang=lang,
                is_admin=is_admin
            )["title"]
        ),
        "unit": obj.unit,
        "photo": obj.photo.file.url if obj.photo else None,
        "created_at": obj.created_at,
    })

    return data
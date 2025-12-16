from rest_framework.exceptions import NotFound
from apps.catalog.models import Subcategory
from apps.core.utils.translations import translate_response


def get_subcategory_detail(*, subcategory_id: int, user, lang: str) -> dict:
    try:
        obj = Subcategory.objects.select_related("category").get(id=subcategory_id)
    except Subcategory.DoesNotExist:
        raise NotFound({"message_key": "subcategory_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["title", "description"],
        lang=lang,
        is_admin=is_admin
    )
    data.update({
        "category_id": obj.category_id,
        "category_name": (
            translate_response(
                obj=obj.category,
                fields=["title"],
                lang=lang,
                is_admin=is_admin
            )["title"]
        ),
        "created_at": obj.created_at,
        "photo": obj.photo.file.url if obj.photo else None
    })

    return data

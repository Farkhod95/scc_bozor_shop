from rest_framework.exceptions import NotFound
from apps.catalog.models import Category
from apps.core.utils.translations import translate_response


def get_category_detail(*, category_id: int, user, lang: str) -> dict:
    try:
        obj = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFound({"message_key": "category_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["title", "description"],
        lang=lang,
        is_admin=is_admin
    )

    data["created_at"] = obj.created_at

    return data

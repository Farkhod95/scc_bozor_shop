from typing import Iterable, Dict, Any
from apps.catalog.models import Category
from apps.core.utils.translations import translate_response


def list_categories(user, lang: str) -> Iterable[Dict[str, Any]]:
    categories = Category.objects.all().order_by("-id")
    is_admin = user.is_staff
    result = []

    for obj in categories:
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

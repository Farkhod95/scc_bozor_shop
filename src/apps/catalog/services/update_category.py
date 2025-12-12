from typing import Dict, Any
from rest_framework.exceptions import NotFound

from apps.catalog.models import Category


def update_category(*, category_id: int, updated_by=None, **fields) -> Dict[str, Any]:
    try:
        obj = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFound({"message_key": "category_not_found"})

    for key, value in fields.items():
        setattr(obj, key, value)

    if updated_by is not None:
        obj.updated_by = updated_by

    obj.save()

    return {
        "id": obj.id,
        "title_uz": obj.title_uz,
        "title_ru": obj.title_ru,
        "title_en": obj.title_en,
        "title_uz_cyrl": obj.title_uz_cyrl,
        "description_uz": obj.description_uz,
        "description_ru": obj.description_ru,
        "description_en": obj.description_en,
        "description_uz_cyrl": obj.description_uz_cyrl,
        "created_at": obj.created_at,
    }

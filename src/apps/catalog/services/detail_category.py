from typing import Dict, Any
from rest_framework.exceptions import NotFound

from apps.catalog.models import Category


def get_category_detail(*, category_id: int) -> Dict[str, Any]:
    try:
        obj = Category.objects.get(id=category_id)
        return {
            "id": obj.id,
            "title": obj.title,
            "description": obj.description,
            "created_at": obj.created_at,
        }
    except Category.DoesNotExist:
        raise NotFound({"message_key": "category_not_found"})
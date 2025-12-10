from typing import Dict, Any
from rest_framework.exceptions import NotFound

from apps.catalog.models import Category


def update_category(*, category_id: int, title: str | None = None, description: str | None = None, updated_by=None) -> Dict[str, Any]:
    try:
        obj = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFound({"detail": "Category not found"})

    if title is not None:
        obj.title = title
    if description is not None:
        obj.description = description
    if updated_by is not None:
        obj.updated_by = updated_by
    obj.save()

    return {
        "id": obj.id,
        "title": obj.title,
        "description": obj.description,
        "created_at": obj.created_at,
    }

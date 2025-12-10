from typing import Dict, Any
from django.db import transaction
from apps.catalog.models import Category


@transaction.atomic
def create_category(title: str, description: str | None = None, created_by=None) -> Dict[str, Any]:
    obj = Category.objects.create(
        title=title,
        description=description,
        created_by=created_by
    )

    return {
        "id": obj.id,
        "title": obj.title,
        "description": obj.description,
        "created_at": obj.created_at,
    }

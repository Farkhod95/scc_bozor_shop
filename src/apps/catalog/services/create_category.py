from typing import Dict, Any
from django.db import transaction
from apps.catalog.models import Category


@transaction.atomic
def create_category(*, created_by=None, **data):
    obj = Category.objects.create(created_by=created_by, **data)
    return {
        "id": obj.id,
        **data,
        "created_at": obj.created_at,
    }
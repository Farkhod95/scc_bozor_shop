from decimal import Decimal
from typing import Dict, Any
from rest_framework.exceptions import ValidationError

from apps.catalog.models import Product, Category


def create_product(category_id: int, name: str, unit: str, created_by) -> Dict[str, Any]:
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValidationError({"message_key": "category_does_not_exist"})

    obj = Product.objects.create(category=category, name=name, unit=unit, created_by=created_by)
    return {
        "id": obj.id,
        "category": obj.category_id,
        "name": obj.name,
        "unit": obj.unit,
        "created_at": obj.created_at,
    }

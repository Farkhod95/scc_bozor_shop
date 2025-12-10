from decimal import Decimal
from typing import Dict, Any
from rest_framework.exceptions import ValidationError, NotFound

from apps.catalog.models import Product, Category


def update_product(*, product_id: int, name: str | None = None, unit: str | None = None, category_id: int | None = None, updated_by=None) -> Dict[str, Any]:
    try:
        obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise NotFound({"message_key": "Product not found"})

    updates: dict[str, Any] = {}

    if name is not None:
        updates["name"] = name

    if unit is not None:
        updates["unit"] = unit

    if category_id is not None:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError({"message_key": "category_does_not_exist"})
        updates["category"] = category

    if updated_by is not None:
        updates["updated_by"] = updated_by

    if updates:
        for key, value in updates.items():
            setattr(obj, key, value)
        obj.save()

    return {
        "id": obj.id,
        "category": obj.category_id,
        "name": obj.name,
        "unit": str(obj.unit),
        "created_at": obj.created_at,
    }

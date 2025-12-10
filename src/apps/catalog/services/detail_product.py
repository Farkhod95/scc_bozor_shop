from typing import Dict, Any

from rest_framework.exceptions import NotFound

from apps.catalog.models import Product


def get_product_detail(*, product_id: int) -> Dict[str, Any]:
    try:
        obj = Product.objects.get(id=product_id)
        return {
            "id": obj.id,
            "category": obj.category_id,
            "name": obj.name,
            "unit": obj.unit,
            "created_at": obj.created_at,
        }
    except Product.DoesNotExist:
        raise NotFound({"message_key": "product_not_found"})
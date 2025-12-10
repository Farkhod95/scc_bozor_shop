from typing import Iterable, Dict, Any
from apps.catalog.models import Product


def list_products() -> Iterable[Dict[str, Any]]:
    products = (
        Product.objects.select_related("category")
        .all()
        .order_by("-id")
        .values("id", "name", "unit", "created_at", "category__id", "category__title")
    )
    result = []
    for product in products:
        result.append({
            "id": product["id"],
            "name": product["name"],
            "unit": product["unit"],
            "category_id": product["category__id"],
            "category_name": product["category__title"],
            "created_at": product["created_at"],
        })
    return result

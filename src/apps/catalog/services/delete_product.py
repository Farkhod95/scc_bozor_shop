from rest_framework.exceptions import NotFound

from apps.catalog.models import Product


def delete_product(product_id: int) -> None:
    try:
        obj = Product.objects.get(id=product_id)
        obj.delete()
    except Product.DoesNotExist:
        raise NotFound({"message_key": "product_not_found"})

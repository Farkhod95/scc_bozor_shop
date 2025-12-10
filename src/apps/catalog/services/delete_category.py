from rest_framework.exceptions import NotFound

from apps.catalog.models import Category


def delete_category(category_id: int) -> None:
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
    except Category.DoesNotExist:
        raise NotFound({"message_key": "category_not_found"})

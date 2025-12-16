from rest_framework.exceptions import NotFound

from apps.catalog.models import Subcategory


def delete_subcategory(subcategory_id: int) -> None:
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        subcategory.delete()
    except Subcategory.DoesNotExist:
        raise NotFound({"message_key": "subcategory_not_found"})

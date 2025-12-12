from rest_framework.exceptions import NotFound

from apps.locations.models import Region


def delete_region(region_id: int) -> None:
    try:
        obj = Region.objects.get(id=region_id)
        obj.delete()
    except Region.DoesNotExist:
        raise NotFound({"message_key": "region_not_found"})

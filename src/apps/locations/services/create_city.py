from rest_framework.exceptions import NotFound

from django.db import transaction
from apps.locations.models import City, Region


@transaction.atomic
def create_city(*, created_by=None, region_id, **data):
    try:
        region = Region.objects.get(pk=region_id)
    except Region.DoesNotExist:
        raise NotFound({"message_key": "region_not_found"})

    obj = City.objects.create(region=region, created_by=created_by, **data)

    return {
        "id": obj.id,
        **data,
        "created_at": obj.created_at,
    }
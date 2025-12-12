from django.db import transaction
from rest_framework.exceptions import NotFound
from apps.locations.models import Region, City


@transaction.atomic
def update_city(*, city_id: int, region_id: int = None, **data):
    try:
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        raise NotFound({"message_key": "city_not_found"})

    if region_id is not None:
        try:
            region = Region.objects.get(pk=region_id)
        except Region.DoesNotExist:
            raise NotFound({"message_key": "region_not_found"})
        city.region = region

    for field, value in data.items():
        setattr(city, field, value)

    city.save(update_fields=["region", *data.keys(), "updated_at"])

    return {
        "id": city.id,
        "region_id": city.region_id,
        **data,
        "created_at": city.created_at,
        "updated_at": city.updated_at,
    }

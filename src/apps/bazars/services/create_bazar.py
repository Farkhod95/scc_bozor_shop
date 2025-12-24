from typing import Dict, Any
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.bazars.models import Bazar, Place
from apps.locations.models import City


@transaction.atomic
def create_bazar(*, city_id: int, address: str, total_places: int, user, **data) -> Dict[str, Any]:
    if Bazar.objects.filter(name_uz=data["name_uz"], city_id=city_id).exists():
        raise ValidationError({"message_key": "bazar_already_exists"})

    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        raise ValidationError({"message_key": "city_not_found"})

    bazar = Bazar.objects.create(
        city=city,
        address=address,
        total_places=total_places,
        created_by=user,
        **data
    )

    _create_places_for_bazar(bazar, total_places)

    return {
        "id": bazar.id,
        "city": bazar.city.name,
        "region": bazar.city.region.name,
        "address": bazar.address,
        "total_places": bazar.total_places,
        **data,
    }



def _create_places_for_bazar(bazar: Bazar, total_places: int) -> None:
    for number in range(1, total_places + 1):
        Place.objects.create(
            bazar=bazar,
            number=number,
        )


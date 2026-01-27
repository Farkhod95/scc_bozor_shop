from typing import Dict, Any
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.bazars.models import Bazar
from apps.accounts.models import User
from apps.locations.models import City


@transaction.atomic
def create_bazar(*, city_id: int, address: str, total_places: int, user, **data) -> Dict[str, Any]:
    if Bazar.objects.filter(name_uz=data["name_uz"], city_id=city_id).exists():
        raise ValidationError({"message_key": "bazar_already_exists"})

    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        raise ValidationError({"message_key": "city_not_found"})

    manager_ids = data.pop("manager_ids", [])
    managers = User.objects.filter(id__in=manager_ids)

    bazar = Bazar.objects.create(
        city=city,
        address=address,
        total_places=total_places,
        created_by=user,
        **data
    )

    if managers.exists():
        bazar.managers.set(managers)

    return {
        "id": bazar.id,
        "city": bazar.city.name,
        "managers": list(managers.values_list('username', flat=True)),
        "region": bazar.city.region.name,
        "address": bazar.address,
        "total_places": bazar.total_places,
        **data,
    }


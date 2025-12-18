from typing import List, Dict
from rest_framework.exceptions import NotFound
from apps.bazars.models import Bazar, Place
from apps.core.services.validate_bazar_admin import validate_bazar_admin


def create_places(*, user, bazar_id: int, count: int = 1) -> List[Dict]:
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise NotFound({"message_key": "bazar_not_found", "message": "Bazar not found"})

    validate_bazar_admin(user, bazar_id)

    created_places = []
    last_number = Place.objects.filter(bazar=bazar).order_by("-number").first()
    start_number = last_number.number + 1 if last_number else 1

    for i in range(count):
        place = Place.objects.create(bazar=bazar, number=start_number + i)
        created_places.append({
            "id": place.id,
            "bazar_id": bazar.id,
            "number": place.number,
            "is_active": place.is_active
        })

    bazar.total_places = Place.objects.filter(bazar=bazar, is_active=True).count()
    bazar.save(update_fields=["total_places"])

    return created_places
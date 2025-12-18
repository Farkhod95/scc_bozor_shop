from rest_framework.exceptions import NotFound
from apps.bazars.models import Place
from apps.core.services.validate_bazar_admin import validate_bazar_admin


def delete_place(user, place_id: int):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise NotFound({"message_key": "place_not_found", "message": "Place not found"})

    validate_bazar_admin(user, place.bazar_id)

    bazar = place.bazar
    place.delete()

    bazar.total_places = Place.objects.filter(bazar=bazar, is_active=True).count()
    bazar.save(update_fields=["total_places"])

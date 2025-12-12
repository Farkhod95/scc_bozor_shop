from rest_framework.exceptions import NotFound
from apps.bazars.models import Place


def delete_place(place_id: int):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise NotFound({"message_key": "place_not_found", "message": "Place not found"})

    bazar = place.bazar
    place.delete()

    bazar.total_places = Place.objects.filter(bazar=bazar, is_active=True).count()
    bazar.save(update_fields=["total_places"])

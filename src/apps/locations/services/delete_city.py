from rest_framework.exceptions import NotFound

from apps.locations.models import City


def delete_city(city_id: int) -> None:
    try:
        category = City.objects.get(id=city_id)
        category.delete()
    except City.DoesNotExist:
        raise NotFound({"message_key": "city_not_found"})

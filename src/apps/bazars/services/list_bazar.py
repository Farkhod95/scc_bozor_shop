from apps.bazars.models import Bazar

def list_bazar(*, city_id: int | None = None):
    qs = Bazar.objects.select_related("city", "city__region").all()

    if city_id is not None:
        qs = qs.filter(city_id=city_id)

    return [
        {
            "id": obj.id,
            "name": obj.name,
            "city": obj.city.name,
            "region": obj.city.region.name,
            "address": obj.address,
            "total_places": obj.total_places,
        }
        for obj in qs
    ]

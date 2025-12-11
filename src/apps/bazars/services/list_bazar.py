from apps.bazars.models import Bazar
from apps.core.utils.dynamic_filters import apply_filters_and_search


def list_bazar(filters=None, search=None):
    queryset = Bazar.objects.select_related("city", "city__region").all()

    search_fields = ["name", "address", "total_places", "city__name", "city__region__name"]
    queryset = apply_filters_and_search(queryset, filters=filters, search=search, search_fields=search_fields)

    return [
        {
            "id": obj.id,
            "name": obj.name,
            "city": obj.city.name,
            "region": obj.city.region.name,
            "address": obj.address,
            "total_places": obj.total_places,
        }
        for obj in queryset
    ]

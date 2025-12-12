from apps.bazars.models import Bazar
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import expand_translated_fields, translate_response


def list_bazar(user, lang: str,filters=None, search=None):
    queryset = Bazar.objects.select_related("city", "city__region").all()

    search_fields = ["name", "address", "total_places"]
    search_fields = expand_translated_fields(Bazar, search_fields)

    queryset = apply_filters_and_search(queryset, filters=filters, search=search, search_fields=search_fields)

    is_admin = user.is_staff

    fields = ["name"]
    result = []
    for obj in queryset:
        data = translate_response(obj, fields=fields, lang=lang, is_admin=is_admin)
        data.update({
            "id": obj.id,
            "city_id": obj.city.id,
            "city": obj.city.name,
            "region": obj.city.region.name,
            "total_places": obj.total_places,
        })
        result.append(data)

    return result
from apps.bazars.models import Bazar
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import expand_translated_fields, translate_response
from geopy.distance import geodesic


def list_bazar(user, lang: str, filters=None, search=None, user_coords=None):
    queryset = Bazar.objects.select_related("city", "city__region").all()

    search_fields = ["name", "address"]
    search_fields = expand_translated_fields(Bazar, search_fields)

    queryset = apply_filters_and_search(queryset, filters=filters, search=search, search_fields=search_fields)

    is_admin = user.is_staff
    fields = ["name"]
    result = []

    for obj in queryset:
        data = translate_response(obj, fields=fields, lang=lang, is_admin=is_admin)

        distance = None
        if user_coords:
            bazar_loc = (obj.lat, obj.lng)
            user_loc = (user_coords['lat'], user_coords['lng'])
            distance = round(geodesic(user_loc, bazar_loc).km, 2)

        images_data = []
        main_image_url = None

        for img in obj.images.all():
            img_url = img.image.file.url if img.image and img.image.file else None
            images_data.append({
                "id": img.id,
                "url": img_url,
                "is_main": img.is_main
            })
            if img.is_main:
                main_image_url = img_url


        data.update({
            "id": obj.id,
            "city_id": obj.city.id,
            "city": obj.city.name,
            "region": obj.city.region.name,
            "total_places": obj.total_places,
            "address": obj.address,
            "lat": obj.lat,
            "lng": obj.lng,
            "average_rating": obj.average_rating,
            "review_count": obj.review_count,
            "distance": distance,
            "main_image": main_image_url,
            "images": images_data
        })
        result.append(data)

    if user_coords:
        result.sort(key=lambda x: x['distance'] if x['distance'] is not None else float('inf'))

    return result
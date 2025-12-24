from apps.bazars.models import Bazar
from apps.core.utils.translations import translate_response
from rest_framework.exceptions import NotFound

def get_bazar_detail(*, bazar_id: int, user, lang: str) -> dict:
    try:
        obj = Bazar.objects.select_related("city", "city__region")\
            .prefetch_related("images__image")\
            .get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise NotFound({"message": "bazar_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["name"],
        lang=lang,
        is_admin=is_admin
    )

    images_list = []
    for img in obj.images.all():
        images_list.append({
            "id": img.id,
            "url": img.image.file.url if img.image and img.image.file else None,
            "is_main": img.is_main
        })

    data.update({
        "id": obj.id,
        "city_id": obj.city.id,
        "city": obj.city.name,
        "region": obj.city.region.name,
        "total_places": obj.total_places,
        "address": obj.address,
        "lat": obj.lat,
        "lng": obj.lng,
        "images": images_list,
        "created_at": obj.created_at
    })

    return data
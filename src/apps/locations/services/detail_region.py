from typing import Dict, Any
from rest_framework.exceptions import NotFound
from apps.locations.models import Region
from apps.core.utils.translations import translate_response


def get_region_detail(*, region_id: int, user, lang: str) -> Dict[str, Any]:
    try:
        obj = Region.objects.get(id=region_id)
    except Region.DoesNotExist:
        raise NotFound({"message_key": "region_not_found"})

    is_admin = user.is_staff

    data = translate_response(
        obj=obj,
        fields=["name"],
        lang=lang,
        is_admin=is_admin
    )

    data.update({
        "id": obj.id,
        "created_at": obj.created_at,
    })

    return data
from typing import Dict, Any
from rest_framework.exceptions import ValidationError, NotFound

from apps.locations.models import Region


def update_region(*, region_id: int, updated_by=None, **fields) -> Dict[str, Any]:

    try:
        obj = Region.objects.get(id=region_id)
    except Region.DoesNotExist:
        raise NotFound({"message_key": "region_not_found"})

    if updated_by:
        fields["updated_by"] = updated_by

    for key, value in fields.items():
        setattr(obj, key, value)

    obj.save()

    return {
        "id": obj.id,
        "name_uz": obj.name_uz,
        "name_ru": obj.name_ru,
        "name_en": obj.name_en,
        "name_uz_cyrl": obj.name_uz_cyrl,
        "created_at": obj.created_at,
    }

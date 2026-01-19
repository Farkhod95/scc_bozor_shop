from typing import Dict, Any

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.bazars.models import Bazar

def update_bazar(*, bazar_id: int, updated_by=None, **fields) -> Dict[str, Any]:
    try:
        bazar = get_object_or_404(Bazar, id=bazar_id)
    except Bazar.DoesNotExist:
        raise ValidationError({"message_key": "bazar_already_exists"})

    if "city_id" in fields:
        fields["city"] = get_object_or_404(Bazar.city.field.related_model, id=fields.pop("city_id"))

    manager_ids = fields.pop("manager_ids", None)

    if updated_by:
        fields["updated_by"] = updated_by

    for key, value in fields.items():
        setattr(bazar, key, value)

    if manager_ids is not None:
        bazar.managers.set(manager_ids)

    bazar.save()

    return {
        "id": bazar.id,
        "name_uz": bazar.name_uz,
        "name_ru": bazar.name_ru,
        "name_en": bazar.name_en,
        "name_uz_cyrl": bazar.name_uz_cyrl,
        "city_id": bazar.city_id,
        "address": bazar.address,
        "total_places": bazar.total_places,
        "lat": bazar.lat,
        "lng": bazar.lng,
        "created_at": bazar.created_at,
    }
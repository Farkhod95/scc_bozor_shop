from typing import Dict
from rest_framework.exceptions import NotFound

from apps.bazars.models import BazarAdmin


def detail_bazar_admin(bazar_admin_id: int) -> Dict:
    try:
        admin = BazarAdmin.objects.select_related("bazar", "user").get(id=bazar_admin_id)
    except BazarAdmin.DoesNotExist:
        raise NotFound({"message_key": "bazar_admin_not_found"})

    return {
        "id": admin.id,
        "bazar_id": admin.bazar.id,
        "bazar_name_uz": getattr(admin.bazar, "name_uz", None),
        "bazar_name_ru": getattr(admin.bazar, "name_ru", None),
        "bazar_name_en": getattr(admin.bazar, "name_en", None),
        "bazar_name_uz_cyrl": getattr(admin.bazar, "name_uz_cyrl", None),
        "user_id": admin.user.id,
        "username": admin.user.username,
        "assigned_at": admin.assigned_at
    }

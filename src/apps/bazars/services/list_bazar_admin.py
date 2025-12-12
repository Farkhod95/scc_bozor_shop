from typing import Iterable, Dict
from apps.bazars.models import BazarAdmin


def list_bazar_admins() -> Iterable[Dict]:
    bazar_admins = BazarAdmin.objects.select_related("bazar", "user").all().order_by("-assigned_at")
    result = []
    for admin in bazar_admins:
        result.append({
            "id": admin.id,
            "bazar_id": admin.bazar.id,
            "bazar_name": getattr(admin.bazar, "name_uz", None),
            "user_id": admin.user.id,
            "username": admin.user.username,
            "assigned_at": admin.assigned_at
        })
    return result

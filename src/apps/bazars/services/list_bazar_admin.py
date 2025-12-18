from typing import Iterable, Dict

from apps.bazars.models import BazarAdmin
from apps.core.utils.dynamic_filters import apply_filters_and_search
from apps.core.utils.translations import expand_translated_fields


def list_bazar_admins(filters=None, search=None) -> Iterable[Dict]:
    queryset = BazarAdmin.objects.select_related("bazar", "user").all().order_by("-assigned_at")

    queryset = apply_filters_and_search(queryset, filters=filters, search=search)

    result = []
    for admin in queryset:
        result.append({
            "id": admin.id,
            "bazar_id": admin.bazar.id,
            "bazar_name": getattr(admin.bazar, "name_uz", None),
            "user_id": admin.user.id,
            "username": admin.user.username,
            "first_name": admin.user.first_name,
            "last_name": admin.user.last_name,
            "assigned_at": admin.assigned_at
        })
    return result

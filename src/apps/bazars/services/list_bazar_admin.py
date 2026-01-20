from typing import Iterable, Dict

from apps.bazars.models import BazarAdmin
from apps.core.services.model_status import UserType
from apps.core.utils.dynamic_filters import apply_filters_and_search


def list_bazar_admins(user, filters=None, search=None) -> Iterable[Dict]:
    queryset = BazarAdmin.objects.select_related("bazar", "user").order_by("-assigned_at").all()

    if user.role == UserType.MANAGER:
        queryset = queryset.filter(bazar__manager=user)

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

from typing import Dict, Any
from rest_framework.exceptions import NotFound, ValidationError

from apps.bazars.models import BazarAdmin, Bazar
from apps.accounts.models import User
from apps.core.services.model_status import UserType


def create_bazar_admin(*, bazar_id: int, user_id: int) -> Dict[str, Any]:
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise NotFound({"message_key": "bazar_not_found"})

    try:
        user = User.objects.get(id=user_id, role=UserType.ADMIN)
    except User.DoesNotExist:
        raise NotFound({"message_key": "user_not_found"})

    if BazarAdmin.objects.filter(bazar=bazar, user=user).exists():
        raise ValidationError({"message_key": "user_already_admin"})

    bazar_admin = BazarAdmin.objects.create(bazar=bazar, user=user)
    return {
        "id": bazar_admin.id,
        "bazar_id": bazar_admin.bazar.id,
        "user_id": bazar_admin.user.id,
        "assigned_at": bazar_admin.assigned_at
    }

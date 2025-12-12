from rest_framework.exceptions import NotFound, ValidationError
from apps.bazars.models import BazarAdmin, Bazar
from apps.accounts.models import User


def update_bazar_admin(*, bazar_admin_id: int, bazar_id: int | None = None, user_id: int | None = None) -> dict:
    try:
        admin = BazarAdmin.objects.get(id=bazar_admin_id)
    except BazarAdmin.DoesNotExist:
        raise NotFound({"message_key": "bazar_admin_not_found"})

    if bazar_id:
        if not Bazar.objects.filter(id=bazar_id).exists():
            raise NotFound({"message_key": "bazar_not_found"})
        admin.bazar_id = bazar_id

    if user_id:
        if not User.objects.filter(id=user_id).exists():
            raise NotFound({"message_key": "user_not_found"})
        admin.user_id = user_id

    if BazarAdmin.objects.filter(bazar_id=admin.bazar_id, user_id=admin.user_id).exclude(id=admin.id).exists():
        raise ValidationError({"message_key": "user_already_admin"})

    admin.save()

    return {
        "id": admin.id,
        "bazar_id": admin.bazar.id,
        "bazar_name": getattr(admin.bazar, "name_uz", None),
        "user_id": admin.user.id,
        "username": admin.user.username,
        "assigned_at": admin.assigned_at
    }

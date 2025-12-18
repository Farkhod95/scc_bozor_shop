from rest_framework.exceptions import PermissionDenied

from apps.core.services.model_status import UserType


def validate_bazar_admin(user, bazar_id):
    if user.role == UserType.SUPERADMIN:
        return
    user_bazar_ids = user.bazaradmin.values_list("bazar_id", flat=True)
    if bazar_id not in user_bazar_ids:
        raise PermissionDenied({"message_key": "not_bazar_admin"})
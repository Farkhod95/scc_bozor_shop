from rest_framework.exceptions import NotFound
from apps.bazars.models import BazarAdmin


def delete_bazar_admin(bazar_admin_id: int):
    try:
        admin = BazarAdmin.objects.get(id=bazar_admin_id)
    except BazarAdmin.DoesNotExist:
        raise NotFound({"message_key": "bazar_admin_not_found"})
    admin.delete()

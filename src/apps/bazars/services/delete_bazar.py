from rest_framework.exceptions import NotFound
from apps.bazars.models import Bazar, Place

def delete_bazar(bazar_id: int):
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise NotFound({"message_key": "bazar_not_found"})

    bazar.delete()
    Place.objects.filter(bazar=bazar).update(is_deleted=True)

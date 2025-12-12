from rest_framework.exceptions import ValidationError
from apps.bazars.models import Bazar, Place

def delete_bazar(bazar_id: int):
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise ValidationError({"message_key": "bazar_does_not_exist"})

    bazar.delete()
    Place.objects.filter(bazar=bazar).update(is_deleted=True)

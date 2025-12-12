from rest_framework.exceptions import ValidationError
from apps.bazars.models import Bazar, Place

def delete_bazar(*, bazar_id: int):
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise ValidationError({"message_kay": "bazar_does_not_exist"})

    Place.objects.filter(bazar=bazar).update(is_delete=True)

from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.bazars.models import BazarImage


@transaction.atomic
def delete_bazar_image(*, image_id: int):
    try:
        bazar_image = BazarImage.objects.select_related("bazar").get(id=image_id)
    except BazarImage.DoesNotExist:
        raise NotFound({"message_key": "bazar_image_not_found"})

    was_main = bazar_image.is_main
    bazar = bazar_image.bazar

    bazar_image.delete()

    if was_main:
        new_main = (
            BazarImage.objects
            .filter(bazar=bazar)
            .order_by("id")
            .first()
        )
        if new_main:
            new_main.is_main = True
            new_main.save(update_fields=["is_main"])

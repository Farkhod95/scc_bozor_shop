from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.bazars.models import Bazar, BazarImage
from apps.uploads.models import File


@transaction.atomic
def create_bazar_image(*, bazar_id: int, image_id: int, is_main: bool = False) -> dict:
    try:
        bazar = Bazar.objects.select_for_update().get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise ValidationError({"message_key": "bazar_not_found"})

    try:
        image = File.objects.get(id=image_id)
    except File.DoesNotExist:
        raise ValidationError({"message_key": "file_not_found"})

    if BazarImage.objects.filter(bazar=bazar, image=image).exists():
        raise ValidationError({"message_key": "image_already_attached"})

    if is_main:
        (
            BazarImage.objects
            .select_for_update()
            .filter(bazar=bazar, is_main=True)
            .update(is_main=False)
        )

    bazar_image = BazarImage.objects.create(
        bazar=bazar,
        image=image,
        is_main=is_main
    )

    return {
        "id": bazar_image.id,
        "bazar_id": bazar.id,
        "image": image.file.url,
        "is_main": bazar_image.is_main,
    }

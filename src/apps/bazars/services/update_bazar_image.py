from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.bazars.models import BazarImage
from apps.uploads.models import File


@transaction.atomic
def update_bazar_image(*, image_id: int, image_file_id: int = None, is_main: bool = None):
    try:
        bazar_image = BazarImage.objects.select_related("bazar", "image").get(id=image_id)
    except BazarImage.DoesNotExist:
        raise NotFound({"message_key": "bazar_image_not_found"})

    if image_file_id:
        file_obj = File.objects.get(id=image_file_id)
        bazar_image.image = file_obj

    if is_main is not None and is_main:
        BazarImage.objects.filter(
            bazar=bazar_image.bazar,
            is_main=True
        ).exclude(id=bazar_image.id).update(is_main=False)
        bazar_image.is_main = True
    elif is_main is not None:
        bazar_image.is_main = False

    bazar_image.save(update_fields=["image", "is_main"] if image_file_id else ["is_main"])

    return {
        "id": bazar_image.id,
        "bazar_id": bazar_image.bazar.id,
        "image": bazar_image.image.file.url if hasattr(bazar_image.image, "file") else None,
        "is_main": bazar_image.is_main,
    }

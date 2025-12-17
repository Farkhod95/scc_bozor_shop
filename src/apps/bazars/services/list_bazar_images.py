from apps.bazars.models import BazarImage


def list_bazar_images(*, bazar_id: int):
    images = (
        BazarImage.objects
        .select_related("image")
        .filter(bazar_id=bazar_id)
        .order_by("-is_main", "-id")
    )

    return [
        {
            "id": image.id,
            "image": image.image.file.url if hasattr(image.image, "file") else None,
            "is_main": image.is_main,
        }
        for image in images
    ]
from rest_framework.exceptions import NotFound, ValidationError

from apps.bazars.models import Place, QRCode
from apps.core.services.validate_bazar_admin import validate_bazar_admin


def create_qrcode(*, user, place_id: int, qr_text: str, created_by=None):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise NotFound({"message_key": "place_not_found"})

    validate_bazar_admin(user, place.bazar_id)

    if hasattr(place, "qrcode"):
        raise ValidationError({"message_key": "qr_exists"})

    qr = QRCode.objects.create(
        place=place,
        qr_text=qr_text,
        created_by=created_by,
        updated_by=created_by
    )

    return {
        "id": qr.id,
        "place_id": place_id,
        "qr_text": qr.qr_text,
        "generate_at": qr.generate_at,
        "valid": qr.valid
    }

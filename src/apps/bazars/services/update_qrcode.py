from rest_framework.exceptions import NotFound
from apps.bazars.models import QRCode

from apps.core.services.validate_bazar_admin import validate_bazar_admin


def update_qrcode(*, user, qrcode_id, place_id: int | None = None, qr_text: str | None = None, valid: bool | None = None, updated_by=None):
    try:
        qr = QRCode.objects.get(id=qrcode_id)
    except QRCode.DoesNotExist:
        raise NotFound({"message_key": "qr_not_found"})

    validate_bazar_admin(user, qr.place.bazar_id)

    if qr_text is not None:
        qr.qr_text = qr_text

    if place_id:
        qr.place_id = place_id

    if valid is not None:
        qr.valid = valid

    qr.updated_by = updated_by
    qr.save()

    return {
        "id": qr.id,
        "place_id": qr.place_id,
        "qr_text": qr.qr_text,
        "generate_at": qr.generate_at,
        "valid": qr.valid,
    }

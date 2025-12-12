from rest_framework.exceptions import NotFound
from apps.bazars.models import QRCode, Place


def get_place_by_qr(*, qr_text: str):
    try:
        qr = QRCode.objects.select_related("place").get(qr_text=qr_text, valid=True)
    except QRCode.DoesNotExist:
        raise NotFound({
            "message_key": "qr_not_found",
            "message": "QR code is invalid or not found"
        })

    place = qr.place

    products = []
    for pp in place.products.select_related("product").all():
        products.append({
            "id": pp.product.id,
            "name": pp.product.name,
            "price": pp.price,
            "quantity": pp.quantity,
        })

    return {
        "id": place.id,
        "bazar_id": place.bazar_id,
        "number": place.number,
        "is_active": place.is_active,
        "qr_code": {
            "qr_text": qr.qr_text,
            "generate_at": qr.generate_at,
            "valid": qr.valid,
        },
        "products": products
    }

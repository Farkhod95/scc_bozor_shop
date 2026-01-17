from typing import Dict
from rest_framework.exceptions import NotFound
from apps.bazars.models import Place, QRCode
from apps.core.utils.translations import translate_response


def detail_place(place_id: int, lang) -> Dict:
    try:
        place = Place.objects.select_related("qrcode").prefetch_related('products', 'products__product', 'products__product__photo').get(id=place_id)
    except Place.DoesNotExist:
        raise NotFound({"message_key": "place_not_found", "message": "Place not found"})

    # QR Code
    try:
        qr = place.qrcode
        qr_data = {
            "qr_text": qr.qr_text,
            "generate_at": qr.generate_at,
            "valid": qr.valid
        }
    except QRCode.DoesNotExist:
        qr_data = None

    # Products
    products = []
    for pp in place.products.all():
        products.append({
            "id": pp.product.id,
            "name": (
                translate_response(
                    obj=pp.product,
                    fields=["name"],
                    lang=lang,
                    is_admin=False
                )["name"]
            ),
            "product_unit": pp.product.unit,
            "price": pp.price,
            "quantity": pp.quantity,
            "photo": pp.product.photo.file.url if pp.product.photo else None,
        })

    return {
        "id": place.id,
        "bazar_id": place.bazar.id,
        "number": place.number,
        "is_active": place.is_active,
        "qr_code": qr_data,
        "products": products
    }

from typing import List, Dict
from apps.bazars.models import Place, QRCode


def list_places(bazar_id, section_id) -> List[Dict]:
    places = Place.objects.all().select_related('qrcode').order_by('number')
    if bazar_id:
        places = places.filter(bazar_id=bazar_id)
    if section_id:
        places = places.filter(section_id=section_id)

    result = []

    for place in places:
        try:
            qr = place.qrcode
            qr_data = {
                "qr_text": qr.qr_text,
                "generate_at": qr.generate_at,
                "valid": qr.valid
            }
        except QRCode.DoesNotExist:
            qr_data = None


        result.append({
            "id": place.id,
            "number": place.number,
            "is_active": place.is_active,
            "slug": place.slug,
            "qr_code": qr_data,
        })

    return result

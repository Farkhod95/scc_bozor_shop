from typing import List, Dict
from rest_framework.exceptions import NotFound
from apps.bazars.models import Place, QRCode
from apps.bazars.models import Bazar


def list_places(bazar_id: int) -> List[Dict]:
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise NotFound({"message_key": "bazar_not_found"})

    places = Place.objects.filter(bazar=bazar).select_related('qrcode').order_by('number')
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
            "qr_code": qr_data,
        })

    return result

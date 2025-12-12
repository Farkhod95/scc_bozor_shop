from typing import Dict, Any

from django.db import transaction

from apps.locations.models import Region


@transaction.atomic
def create_region(*, created_by=None, **data) -> Dict[str, Any]:
    obj = Region.objects.create(
        created_by=created_by,
        **data
    )

    return {
        "id": obj.id,
        "code": obj.code,
        "created_at": obj.created_at,
        **data
    }

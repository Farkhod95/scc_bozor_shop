from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.catalog.models import Subcategory
from apps.uploads.models import File


@transaction.atomic
def create_subcategory(*, created_by=None, **data):
    try:
        photo = File.objects.get(id=data.pop("photo_id"))
    except File.DoesNotExist:
        raise ValidationError({"message_key": "file_not_found"})

    obj = Subcategory.objects.create(created_by=created_by, photo=photo, **data)
    return {
        "id": obj.id,
        **data,
        "created_at": obj.created_at,
    }
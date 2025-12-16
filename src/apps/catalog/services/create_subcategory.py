from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.catalog.models import Subcategory, Category
from apps.uploads.models import File


@transaction.atomic
def create_subcategory(*, created_by=None, **data):
    category_id = data.pop("category_id", None)
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValidationError({"message_key": "category_does_not_exist"})

    try:
        photo = File.objects.get(id=data.pop("photo_id"))
    except File.DoesNotExist:
        raise ValidationError({"message_key": "file_not_found"})

    obj = Subcategory.objects.create(created_by=created_by, category=category, photo=photo, **data)
    return {
        "id": obj.id,
        **data,
        "created_at": obj.created_at,
    }
from typing import Dict, Any

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.catalog.models import Product, Category, Subcategory
from apps.uploads.models import File


@transaction.atomic
def create_product(*, created_by=None, **data) -> Dict[str, Any]:
    category_id = data.pop("category_id", None)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValidationError({"message_key": "category_does_not_exist"})

    try:
        subcategory = Subcategory.objects.get(id=data.pop("subcategory_id"))
    except Subcategory.DoesNotExist:
        raise ValidationError({"message_key": "category_does_not_exist"})

    try:
        photo = File.objects.get(id=data.pop("photo_id"))
    except File.DoesNotExist:
        raise ValidationError({"message_key": "file_not_found"})


    obj = Product.objects.create(
        category=category,
        subcategory=subcategory,
        created_by=created_by,
        photo=photo,
        **data
    )

    return {
        "id": obj.id,
        "category": obj.category_id,
        "created_at": obj.created_at,
        **data
    }

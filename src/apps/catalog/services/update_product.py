from typing import Dict, Any
from rest_framework.exceptions import ValidationError, NotFound
from apps.catalog.models import Product, Category
from apps.uploads.models import File


def update_product(*, product_id: int, category_id: int | None = None, updated_by=None, **fields) -> Dict[str, Any]:
    obj = Product.objects.filter(id=product_id).first()
    if not obj:
        raise NotFound({"message_key": "product_not_found"})

    if category_id is not None:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValidationError({"message_key": "category_does_not_exist"})
        fields["category"] = category

    if updated_by is not None:
        fields["updated_by"] = updated_by

    photo = fields.pop("photo_id", None)
    if photo:
        try:
            photo = File.objects.get(id=fields.pop("photo_id"))
            obj.photo = photo
        except File.DoesNotExist:
            raise ValidationError({"message_key": "file_not_found"})


    for key, value in fields.items():
        if value is not None:
            setattr(obj, key, value)
    obj.save()

    return {
        "id": obj.id,
        "category": obj.category_id,
        "name_uz": obj.name_uz,
        "name_ru": obj.name_ru,
        "name_en": obj.name_en,
        "name_uz_cyrl": obj.name_uz_cyrl,
        "unit": str(obj.unit),
        "created_at": obj.created_at,
    }

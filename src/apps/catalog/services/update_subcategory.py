from typing import Dict, Any
from rest_framework.exceptions import NotFound, ValidationError

from apps.catalog.models import Subcategory, Category
from apps.uploads.models import File


def update_subcategory(*, subcategory_id: int, category_id: int | None = None, updated_by=None, **fields) -> Dict[str, Any]:
    try:
        obj = Subcategory.objects.get(id=subcategory_id)
    except Subcategory.DoesNotExist:
        raise NotFound({"message_key": "subcategory_not_found"})


    if category_id is not None:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValidationError({"message_key": "category_does_not_exist"})
        fields["category"] = category

    photo = fields.pop("photo_id", None)
    if photo:
        try:
            photo = File.objects.get(id=fields.pop("photo_id"))
            obj.photo = photo
        except File.DoesNotExist:
            raise ValidationError({"message_key": "file_not_found"})

    for key, value in fields.items():
        setattr(obj, key, value)

    if updated_by is not None:
        obj.updated_by = updated_by

    obj.save()

    return {
        "id": obj.id,
        "title_uz": obj.title_uz,
        "title_ru": obj.title_ru,
        "title_en": obj.title_en,
        "title_uz_cyrl": obj.title_uz_cyrl,
        "description_uz": obj.description_uz,
        "description_ru": obj.description_ru,
        "description_en": obj.description_en,
        "description_uz_cyrl": obj.description_uz_cyrl,
        "created_at": obj.created_at,
    }

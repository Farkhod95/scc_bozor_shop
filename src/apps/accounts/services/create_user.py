from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from apps.core.services.model_status import UserType
from apps.uploads.models import File

User = get_user_model()


@transaction.atomic
def create_user(user, **validated_data) -> dict:
    username = validated_data.get("username")
    if User.objects.all_with_deleted().filter(username=username).exists():
        raise ValidationError({"message_key": "username_already_taken"})
    password = validated_data.pop("password")
    profile_image_id = validated_data.pop("profile_image", None)

    profile_image = None
    if profile_image_id:
        try:
            profile_image = File.objects.get(id=profile_image_id)
        except File.DoesNotExist:
            raise ValidationError({"message_key": "file_not_found"})

    role = validated_data.pop("role", None)

    if role and role != UserType.ADMIN and not user.is_superuser:
        raise ValidationError({"message_key": "permission_denied"})

    new_user = User.objects.create(
        **validated_data,
        password=make_password(password),
        profile_image=profile_image,
        role=role or UserType.ADMIN,
        is_staff=True,
        created_by=user
    )

    return {
        "id": new_user.id,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "phone_number": new_user.phone_number,
        "profile_image": new_user.profile_image.file.url if new_user.profile_image else None,
        "role": new_user.role,
    }
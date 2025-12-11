from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from apps.core.services.model_status import UserType
from apps.uploads.models import File

User = get_user_model()


@transaction.atomic
def create_user(**validated_data) -> dict:
    username = validated_data.get("username")
    if User.objects.filter(username=username).exists():
        raise ValidationError({"message_key": "username_already_taken"})

    password = validated_data.pop("password")
    profile_image_id = validated_data.pop("profile_image", None)

    profile_image = None
    if profile_image_id:
        try:
            profile_image = File.objects.get(id=profile_image_id)
        except File.DoesNotExist:
            raise ValidationError({"message_key": "file_not_found"})

    user = User.objects.create(
        **validated_data,
        password=make_password(password),
        profile_image=profile_image,
        role=UserType.ADMIN,
        is_staff=True,
    )

    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "profile_image": user.profile_image.file.url if user.profile_image else None,
        "role": user.role,
    }

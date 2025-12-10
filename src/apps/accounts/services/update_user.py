from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from apps.uploads.models import File

User = get_user_model()


@transaction.atomic
def update_user(user_id: int, **validated_data) -> dict:
    user = _get_user(user_id)

    _update_username_and_password(user,
                                  username=validated_data.get("username"),
                                  password=validated_data.get("password"))

    _update_profile_image(user, profile_image_id=validated_data.get("profile_image"))

    _update_other_fields(user, validated_data)

    user.save()

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

def _get_user(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError({"message_key": "user_not_found"})


def _update_username_and_password(user: User, username: str = None, password: str = None):
    if username and username != user.username:
        if User.objects.filter(username=username).exists():
            raise ValidationError({"message_key": "username_already_taken"})
        user.username = username
    if password:
        user.password = make_password(password)


def _update_profile_image(user: User, profile_image_id: int = None):
    if profile_image_id is not None:
        if profile_image_id == 0:
            user.profile_image = None
        else:
            try:
                file_obj = File.objects.get(id=profile_image_id)
                user.profile_image = file_obj
            except File.DoesNotExist:
                raise ValidationError({"message_key": "file_not_found"})


def _update_other_fields(user: User, validated_data: dict):
    for field in ["first_name", "last_name", "email", "phone_number"]:
        if field in validated_data:
            setattr(user, field, validated_data[field])

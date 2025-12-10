from apps.accounts.models import User


def get_profile_data(user: User) -> dict:
    return {
        "username": user.username,
        "phone": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "language": user.language,
        "profile_image": user.profile_image.file.url if user.profile_image else None,
    }
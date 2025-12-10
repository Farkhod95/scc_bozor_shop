from django.contrib.auth import get_user_model

User = get_user_model()

def list_users(user) -> list[dict]:
    users = User.objects.filter(created_by=user)
    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "profile_image": user.profile_image.file.url if user.profile_image else None,
        })

    return result

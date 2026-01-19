from django.contrib.auth import get_user_model

from apps.core.services.model_status import UserType
from apps.core.utils.dynamic_filters import apply_filters_and_search

User = get_user_model()

def list_users(user, filters, search):
    queryset = User.objects.select_related("profile_image").all()
    if user.role == UserType.MANAGER:
        queryset = queryset.filter(created_by=user)
    search_fields = ["username", "first_name", "last_name", "email"]
    queryset = apply_filters_and_search(queryset, filters=filters, search=search, search_fields=search_fields)

    return [
        {
            "id": u.id,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "phone_number": u.phone_number,
            "role": u.role,
            "profile_image": u.profile_image.file.url if u.profile_image else None,
        }
        for u in queryset
    ]

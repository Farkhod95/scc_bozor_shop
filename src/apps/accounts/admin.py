from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "role",
        "language",
        "is_staff",
        "is_active",
    )

    list_filter = ("role", "language", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Permissions", {
            "fields": (
                "role",
                "language",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": ("last_login", )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "role",
                "language",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions")

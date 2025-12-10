from django.contrib import admin
from .models import *


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    search_fields = ["user__phone_number"]
    list_display = ("id", "file", "created_at", "updated_at")
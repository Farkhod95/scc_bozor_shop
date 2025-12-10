from django.contrib import admin
from apps.locations.models import Region, City

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")
    search_fields = ("name", "region__name")
    list_filter = ("region",)

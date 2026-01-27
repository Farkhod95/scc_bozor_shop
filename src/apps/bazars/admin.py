from django.contrib import admin
from apps.bazars.models import Bazar, BazarAdmin, Place, PlacePriceHistory, QRCode, BazarImage, BazarSection
from apps.bazars.models.place_product import PlaceProduct


class BazarImageInline(admin.TabularInline):
    model = BazarImage
    extra = 1


@admin.register(Bazar)
class BazarAdminPanel(admin.ModelAdmin):
    inlines = [BazarImageInline]
    list_display = ("id", "name", "city", "address", "total_places")
    search_fields = ("name", "address")
    list_filter = ("city",)

@admin.register(BazarAdmin)
class BazarAdminUserPanel(admin.ModelAdmin):
    list_display = ("id", "bazar", "user", "assigned_at")
    search_fields = ("user__username", "bazar__name")
    list_filter = ("assigned_at",)

@admin.register(BazarSection)
class BazarSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "svg", "bazar")
    search_fields = ("name", "svg__file")
    list_filter = ("bazar",)

class PlaceProductInline(admin.TabularInline):
    model = PlaceProduct
    extra = 1
    fields = ("product", "price", "quantity")
    autocomplete_fields = ("product",)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "bazar", "number", "slug", "is_active")
    search_fields = ("bazar__name", "number", "slug")
    list_filter = ("bazar", "is_active")
    inlines = [PlaceProductInline]

@admin.register(PlaceProduct)
class PlaceProductAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "product", "price", "quantity")
    search_fields = ("place__number", "product__name", "place__bazar__name")
    list_filter = ("place__bazar",)


@admin.register(PlacePriceHistory)
class PlacePriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "product", "price", "recorded_at")
    search_fields = ("place__bazar__name", "product__name")
    list_filter = ("recorded_at",)

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "qr_text", "generate_at", "valid")
    search_fields = ("qr_text",)
    list_filter = ("valid",)

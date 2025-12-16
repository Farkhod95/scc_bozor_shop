from django.contrib import admin
from apps.catalog.models import Category, Product, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "photo")
    search_fields = ("title",)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "photo", "category")
    search_fields = ("title",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "subcategory", "unit", "photo")
    search_fields = ("name", "category__title", "subcategory__title")
    list_filter = ("category", "subcategory", "unit")

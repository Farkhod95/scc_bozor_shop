from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category, Subcategory

@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(Subcategory)
class CategoryTranslation(TranslationOptions):
    fields = ('title', 'description')


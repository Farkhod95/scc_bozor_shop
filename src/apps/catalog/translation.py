from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category

@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('title', 'description')


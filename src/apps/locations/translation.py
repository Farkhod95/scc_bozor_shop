from modeltranslation.translator import register, TranslationOptions
from .models import Region, City

@register(Region)
class RegionTranslation(TranslationOptions):
    fields = ('name',)

@register(City)
class CityTranslation(TranslationOptions):
    fields = ('name',)

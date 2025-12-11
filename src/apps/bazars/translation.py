from modeltranslation.translator import register, TranslationOptions
from .models import Bazar

@register(Bazar)
class BazarTranslation(TranslationOptions):
    fields = ('name',)

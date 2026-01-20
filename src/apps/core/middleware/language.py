from django.utils.deprecation import MiddlewareMixin


class LanguageMiddleware(MiddlewareMixin):
    SUPPORTED_LANGUAGES = ['en', 'uz', 'uz_cyrl', 'ru']

    def process_request(self, request):
        lang = request.headers.get('Accept-Language') or request.GET.get('lang') or 'en'
        lang = lang.lower().replace('-', '_')

        if lang not in self.SUPPORTED_LANGUAGES:
            lang = 'en'

        request.lang = lang
from rest_framework.response import Response


class ResponseController:
    def __init__(self, request):
        self.request = request

    success_message: dict = {"en": "OK", "uz": "OK", "uz-cyrl": "OK", "ru": "OK"}
    error_message: dict = {"en": "", "uz": "", "uz-cyrl": "", "ru": ""}
    exception: str = ""

    def success_response(self, message=None, status=200, **extra_data):
        if message is None:
            message = self.success_message

        lang = self.request.lang
        message_by_lang = message.get(lang)
        response = {"message": message_by_lang}
        if extra_data:
            response.update({key: extra_data[key] for key in extra_data})
        return Response(response, status=status)

    def error_response(self, exception=None):
        lang = self.request.lang
        error_by_lang = self.error_message.get(lang)

        response = {"detail": error_by_lang}
        if exception:
            response["detail"] = exception
        return Response(response, status=400)

    def error_response_with_exception(self, exception, status=400):
        lang = self.request.lang
        exception_by_lang = exception.get(lang)
        response = {"detail": exception_by_lang}
        return Response(response, status=status)

    # Aliases to satisfy interfaces expecting success()/error()
    # Keep backward compatibility with existing code using success_response/error_response
    def success(self, message=None, status=200, **extra_data):
        return self.success_response(message=message, status=status, **extra_data)

    def error(self, exception=None):
        return self.error_response(exception=exception)
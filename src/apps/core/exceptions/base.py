from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied, NotAuthenticated, \
    AuthenticationFailed

from apps.core.exceptions.error_responses import ERROR_MESSAGES


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    request = context.get("request")
    lang = getattr(request, "lang", "en")

    detail = getattr(exc, "detail", None)

    if not isinstance(detail, dict):
        return Response({
            "detail": str(detail) if detail else str(exc),
        }, status=getattr(exc, "status_code", response.status_code))

    message_key = detail.get("message_key")
    if message_key and message_key in ERROR_MESSAGES:
        localized_message = ERROR_MESSAGES.get(message_key).get(lang, ERROR_MESSAGES.get(message_key).get("en"))
    else:
        localized_message = detail

    if isinstance(exc, ValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, NotFound):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, PermissionDenied):
        status_code = status.HTTP_403_FORBIDDEN
    else:
        status_code = response.status_code

    return Response({
        "detail": localized_message,
    }, status=status_code)
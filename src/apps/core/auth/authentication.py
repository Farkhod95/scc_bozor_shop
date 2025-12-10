from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from apps.core.auth.jwt import JWTService

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT auth using the Authorization header.
    Header format:
        Authorization: Bearer <access_token>
    """

    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization")

        if not header:
            return None  # Allows other authenticators or unauth access

        parts = header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed("Invalid authorization header")

        token = parts[1]

        try:
            payload = JWTService.decode(token)
        except ValueError as e:
            raise exceptions.AuthenticationFailed(str(e))

        if payload.get("type") != "access":
            raise exceptions.AuthenticationFailed("Invalid token type")

        user = User.objects.filter(id=payload.get("user_id"), is_active=True).first()
        if not user:
            raise exceptions.AuthenticationFailed("User not found")

        return user, None

    def authenticate_header(self, request):
        return 'Bearer'
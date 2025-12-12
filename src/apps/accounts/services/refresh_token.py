from rest_framework.exceptions import AuthenticationFailed

from apps.core.auth.jwt import JWTService


def refresh_access_token(*, refresh_token: str) -> dict:
    try:
        tokens = JWTService.refresh_access_token(refresh_token)
        access_token = tokens["access"]
    except ValueError as e:
        raise AuthenticationFailed(detail=str(e))
    return {"access": access_token}
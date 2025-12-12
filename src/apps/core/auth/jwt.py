import datetime
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class JWTService:
    ACCESS_LIFETIME = datetime.timedelta(hours=1)
    REFRESH_LIFETIME = datetime.timedelta(days=100)

    @staticmethod
    def _generate(payload: dict, lifetime: datetime.timedelta) -> str:
        current_time = datetime.datetime.utcnow()
        expire_time = current_time + lifetime

        payload = {**payload, "exp": expire_time, "iat": current_time}

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    @classmethod
    def create_tokens(cls, user_id: int) -> dict:
        access = cls._generate({"user_id": user_id, "type": "access"}, cls.ACCESS_LIFETIME)
        refresh = cls._generate({"user_id": user_id, "type": "refresh"}, cls.REFRESH_LIFETIME)
        return {"access": access, "refresh": refresh}

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")


    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> dict:
        payload = cls.decode(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Token is not a refresh token")

        user_id = payload.get("user_id")
        new_access = cls._generate({"user_id": user_id, "type": "access"}, cls.ACCESS_LIFETIME)
        return {"access": new_access}
from .base import *

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "bazar_user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "bazar_pass"),
        "HOST": os.environ.get("SQL_HOST", "bazardb"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

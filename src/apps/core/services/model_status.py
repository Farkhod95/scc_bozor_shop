from django.db import models


class LanguageType(models.TextChoices):
    EN = "en", "En"
    UZ = "uz", "Uz"
    UZ_CYRL = "uz-cyrl", "Uz-Cyrl"
    RU = "ru", "Ru"

class UserType(models.TextChoices):
    SUPERADMIN = "superadmin", "Superadmin"
    MANAGER = "manager", "Manager"
    ADMIN = "admin", "Admin"
    USER = "user", "User"

class UnitType(models.TextChoices):
    PIECE = "pcs", "Piece"
    KILOGRAM = "kg", "Kilogram"
    GRAM = "g", "Gram"
    LITER = "l", "Liter"
    MILLILITER = "ml", "Milliliter"
    METER = "m", "Meter"
    CENTIMETER = "cm", "Centimeter"
    PACK = "pack", "Pack"
    BOX = "box", "Box"
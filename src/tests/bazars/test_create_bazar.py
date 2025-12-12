from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Bazar
from apps.locations.models import City

User = get_user_model()


class TestCreateBazarAPI(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
    ]

    def setUp(self):
        # SuperAdmin user
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        # Normal user
        self.normal_user = User.objects.get(id=2)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.url = "/api/bazars/v1/bazar/create/"
        self.city = City.objects.get(id=1)

        self.valid_payload = {
            "name_uz": "Yangi Bazar",
            "city_id": self.city.id,
            "address": "Toshkent ko'chasi 12",
            "total_places": 50,
        }

        self.invalid_payload = {
            "name": "",
            "city_id": 9999,
        }

    def test_create_bazar_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()["data"]

        self.assertEqual(data["name_uz"], "Yangi Bazar")
        self.assertEqual(data["city"], self.city.name)
        self.assertEqual(data["total_places"], 50)

    def test_create_bazar_duplicate_name(self):
        Bazar.objects.create(
            name_uz="Yangi Bazar",
            city=self.city,
            address="Test address",
            total_places=20
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.json())

    def test_create_bazar_normal_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_bazar_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_bazar_invalid_city(self):
        payload = {
            "name": "Test Bazar",
            "city_id": 9999,
            "address": "Test address",
            "total_places": 10,
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

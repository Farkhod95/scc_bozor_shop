from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestUpdateBazarAPI(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        # Normal user
        self.normal_user = User.objects.get(id=2)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.base_url = "/api/bazars/v1/bazar/"

    def test_update_bazar_success(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/update/"

        payload = {
            "name_uz": "Yangilangan Bazar",
            "address": "Yangi manzil 123",
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]
        self.assertEqual(data["name_uz"], "Yangilangan Bazar")
        self.assertEqual(data["address"], "Yangi manzil 123")

    def test_update_bazar_forbidden_for_normal_user(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/update/"

        payload = {"name_uz": "No Access"}

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_bazar_unauthenticated(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/update/"

        self.client.credentials()
        response = self.client.patch(url, {"name_uz": "X"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_bazar_not_found(self):
        url = f"{self.base_url}9999/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, {"name_uz": "X"}, format="json")

        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST])

    def test_update_bazar_invalid_city(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/update/"

        payload = {"city_id": 9999}

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, payload, format="json")

        # City not found should be 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

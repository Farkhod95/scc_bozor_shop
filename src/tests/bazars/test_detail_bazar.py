from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestDetailBazarAPI(APITestCase):
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

    def test_bazar_detail_success_superadmin(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]
        self.assertIn("city", data)
        self.assertIn("total_places", data)

    def test_bazar_detail_success_normal_user(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bazar_detail_unauthenticated_allowed(self):
        bazar_id = 1
        url = f"{self.base_url}{bazar_id}/detail/"

        self.client.credentials()
        response = self.client.get(url)

        # Detail view has no permission classes, should be accessible
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bazar_detail_not_found(self):
        url = f"{self.base_url}9999/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

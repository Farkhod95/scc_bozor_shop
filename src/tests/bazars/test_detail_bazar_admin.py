from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestDetailBazarAdminAPI(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
        "tests/bazars/fixtures/bazar_admins.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.super_access = tokens["access"]

        # normal user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.base_url = "/api/bazars/v1/bazar-admin/"
        self.bazar_admin_id = 1

    def test_detail_bazar_admin_success(self):
        url = f"{self.base_url}{self.bazar_admin_id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("data", response.data)
        data = response.data["data"]

        self.assertEqual(data["id"], self.bazar_admin_id)
        self.assertIn("bazar_id", data)
        self.assertIn("bazar_name_uz", data)
        self.assertIn("user_id", data)
        self.assertIn("username", data)
        self.assertIn("assigned_at", data)

    def test_detail_bazar_admin_not_found(self):
        url = f"{self.base_url}9999/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_bazar_admin_forbidden_for_normal_user(self):
        url = f"{self.base_url}{self.bazar_admin_id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_bazar_admin_unauthenticated(self):
        url = f"{self.base_url}{self.bazar_admin_id}/detail/"

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

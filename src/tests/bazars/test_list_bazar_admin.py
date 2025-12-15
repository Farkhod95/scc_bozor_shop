from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestListBazarAdminAPI(APITestCase):
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

        self.base_url = "/api/bazars/v1/bazar-admin/list/"

    def test_list_bazar_admins_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("data", response.data)
        self.assertTrue(len(response.data["data"]) > 0)

        item = response.data["data"][0]

        self.assertIn("id", item)
        self.assertIn("bazar_id", item)
        self.assertIn("bazar_name", item)
        self.assertIn("user_id", item)
        self.assertIn("username", item)
        self.assertIn("assigned_at", item)

    def test_list_bazar_admins_forbidden_for_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_bazar_admins_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

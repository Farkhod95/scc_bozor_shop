from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Bazar, BazarAdmin

User = get_user_model()


class TestUpdateBazarAdminAPI(APITestCase):
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

        self.bazar_admin = BazarAdmin.objects.get(id=2)
        self.new_bazar = Bazar.objects.exclude(id=self.bazar_admin.bazar_id).first()

        self.base_url = "/api/bazars/v1/bazar-admin/"

        self.payload = {
            "bazar_id": self.new_bazar.id,
            "user_id": self.bazar_admin.user_id,
        }

    def test_update_bazar_admin_success(self):
        url = f"{self.base_url}{self.bazar_admin.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.bazar_admin.refresh_from_db()
        self.assertEqual(self.bazar_admin.bazar_id, self.new_bazar.id)

    def test_update_bazar_admin_not_found(self):
        url = f"{self.base_url}9999/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_bazar_admin_forbidden_for_normal_user(self):
        url = f"{self.base_url}{self.bazar_admin.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_bazar_admin_unauthenticated(self):
        url = f"{self.base_url}{self.bazar_admin.id}/update/"

        self.client.credentials()
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

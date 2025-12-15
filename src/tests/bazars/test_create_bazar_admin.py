from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Bazar, BazarAdmin

User = get_user_model()


class TestCreateBazarAdminAPI(APITestCase):
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
        self.super_access = tokens["access"]

        # normal user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        # target user (bazar admin bo‘ladigan)
        self.target_user = User.objects.get(id=2)

        self.bazar = Bazar.objects.get(id=1)

        self.base_url = "/api/bazars/v1/bazar-admin/create/"

        self.payload = {
            "bazar_id": self.bazar.id,
            "user_id": self.target_user.id,
        }

    def test_create_bazar_admin_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            BazarAdmin.objects.filter(
                bazar_id=self.bazar.id,
                user_id=self.target_user.id
            ).exists()
        )

    def test_create_bazar_admin_forbidden_for_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_bazar_admin_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_bazar_admin_bazar_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")

        payload = {
            "bazar_id": 9999,
            "user_id": self.target_user.id,
        }

        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_bazar_admin_user_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")

        payload = {
            "bazar_id": self.bazar.id,
            "user_id": 9999,
        }

        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
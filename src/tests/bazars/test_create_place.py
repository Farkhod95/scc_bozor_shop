from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Bazar, Place

User = get_user_model()


class TestCreatePlaceAPI(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
        "tests/bazars/fixtures/places.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        super_tokens = JWTService.create_tokens(self.superadmin.id)
        self.super_access = super_tokens["access"]

        # Bazar Admin
        self.bazar_admin = User.objects.get(id=2)
        admin_tokens = JWTService.create_tokens(self.bazar_admin.id)
        self.admin_access = admin_tokens["access"]

        # normal user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.bazar = Bazar.objects.get(id=1)
        self.base_url = "/api/bazars/v1/place/create/"

    def test_create_places_success_by_superadmin(self):
        payload = {
            "bazar_id": self.bazar.id,
            "count": 2,
        }

        existing_count = Place.objects.filter(bazar_id=self.bazar.id).count()

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Place.objects.filter(bazar_id=self.bazar.id).count(),
            existing_count + 2
        )

    def test_create_places_success_by_bazar_admin(self):
        payload = {
            "bazar_id": self.bazar.id,
            "count": 1,
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Place.objects.filter(bazar_id=self.bazar.id).exists()
        )

    def test_create_places_forbidden_for_normal_user(self):
        payload = {
            "bazar_id": self.bazar.id,
            "count": 1,
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_places_unauthenticated(self):
        payload = {
            "bazar_id": self.bazar.id,
            "count": 1,
        }

        self.client.credentials()
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_places_bazar_not_found(self):
        payload = {
            "bazar_id": 9999,
            "count": 1,
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_places_validation_error(self):
        payload = {
            "bazar_id": self.bazar.id,
            "count": 0,  # min_value=1
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

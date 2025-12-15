from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Bazar, Place

User = get_user_model()


class TestListPlaceAPI(APITestCase):
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
        self.base_url = "/api/bazars/v1/place/list/?bazar_id=1"

    def test_list_places_success_by_superadmin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertTrue(len(response.data["data"]) > 0)

        place = response.data["data"][0]
        self.assertIn("id", place)
        self.assertIn("number", place)
        self.assertIn("is_active", place)


    def test_list_places_bazar_filter(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(self.base_url, {"bazar_id": self.bazar.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for place in response.data["data"]:
            self.assertEqual(place["is_active"], self.bazar.id)

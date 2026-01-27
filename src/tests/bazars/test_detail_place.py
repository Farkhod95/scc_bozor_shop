from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Place

User = get_user_model()


class TestDetailPlaceAPI(APITestCase):
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

        self.place = Place.objects.get(id=1)
        self.base_url = "/api/bazars/v1/place/"

    def test_detail_place_success_by_superadmin(self):
        url = f"{self.base_url}{self.place.slug}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]

        self.assertEqual(data["id"], self.place.id)
        self.assertEqual(data["bazar_id"], self.place.bazar_id)
        self.assertEqual(data["number"], self.place.number)
        self.assertEqual(data["is_active"], self.place.is_active)

    def test_detail_place_success_by_non_user(self):
        url = f"{self.base_url}{self.place.slug}/detail/"

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["id"], self.place.id)

    def test_detail_place_not_found(self):
        url = f"{self.base_url}9999/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


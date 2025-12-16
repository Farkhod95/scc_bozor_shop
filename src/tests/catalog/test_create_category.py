from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.catalog.models import Category

User = get_user_model()


class TestCreateCategoryAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/files.json",
        "tests/catalog/fixtures/categories.json",
    ]

    def setUp(self):
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.url = "/api/catalog/v1/category/create/"

        self.valid_payload = {
            "title_uz": "Electronics",
            "description_uz": "All tech products",
            "photo_id": 1,
        }

        self.invalid_payload = {
            "title": "",
        }

    def test_create_category_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["data"]["title_uz"], "Electronics")
        self.assertTrue(Category.objects.filter(title="Electronics").exists())

    def test_create_category_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_non_superadmin_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_invalid_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

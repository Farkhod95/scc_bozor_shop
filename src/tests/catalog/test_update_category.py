from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.catalog.models import Category

User = get_user_model()


class TestUpdateCategoryAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/categories.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        self.tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = self.tokens["access"]

        # Normal user
        self.normal_user = User.objects.get(id=3)
        self.normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = self.normal_tokens["access"]

        self.base_url = "/api/catalog/v1/category/"
        self.category = Category.objects.get(id=1)

        self.valid_payload = {
            "title": "Updated Title",
            "description": "Updated description",
        }


    def test_update_category_success(self):
        url = f"{self.base_url}{self.category.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["id"], self.category.id)

    def test_update_category_normal_user_forbidden(self):
        url = f"{self.base_url}{self.category.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_unauthenticated(self):
        url = f"{self.base_url}{self.category.id}/update/"

        self.client.credentials()
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_category_not_found(self):
        url = "/api/catalog/v1/categories/9999/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

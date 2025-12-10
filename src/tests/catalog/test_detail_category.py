from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestCategoryDetailAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/categories.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        # Normal user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.base_url = "/api/catalog/v1/category/"

    def test_category_detail_success(self):
        category_id = 1
        url = f"{self.base_url}{category_id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["data"]["id"], category_id)

    def test_category_detail_normal_user_allowed(self):
        category_id = 1
        url = f"{self.base_url}{category_id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail_unauthenticated(self):
        category_id = 1
        url = f"{self.base_url}{category_id}/detail/"

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_detail_not_found(self):
        url = f"{self.base_url}9999/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

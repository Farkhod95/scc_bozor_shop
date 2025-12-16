from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.catalog.models import Product, Category, Subcategory

User = get_user_model()


class TestCreateProductAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/files.json",
        "tests/catalog/fixtures/categories.json",
        "tests/catalog/fixtures/subcategories.json",
        "tests/catalog/fixtures/products.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.url = "/api/catalog/v1/product/create/"

        self.category = Category.objects.get(id=1)
        self.subcategory = Subcategory.objects.get(id=1)

        self.valid_payload = {
            "name_uz": "New Product",
            "unit": "kg",
            "photo_id": 1,
            "category_id": self.category.id,
            "subcategory_id": self.subcategory.id,
        }

        self.invalid_payload = {
            "name": "",
            "unit": "kg",
        }

    def test_create_product_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()["data"]

        self.assertEqual(data["name_uz"], "New Product")
        self.assertEqual(data["category"], self.category.id)

    def test_create_product_normal_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_category_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

        payload = {
            "name": "Product X",
            "unit": "kg",
            "category_id": 9999,
            "subcategory_id": 9999,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND])

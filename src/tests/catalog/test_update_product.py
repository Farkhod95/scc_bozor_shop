from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.catalog.models import Product, Category

User = get_user_model()


class TestUpdateProductAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/categories.json",
        "tests/catalog/fixtures/products.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        # user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.base_url = "/api/catalog/v1/product/"
        self.product = Product.objects.get(id=1)
        self.category = Category.objects.get(id=1)

        self.valid_payload = {
            "name": "Updated Product",
            "price": "20000.00",
            "category_id": self.category.id,
        }

        self.invalid_payload = {
            "category_id": "1111",
        }

    def test_update_product_success(self):
        url = f"{self.base_url}{self.product.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["name"], "Updated Product")
        self.assertEqual(data["id"], self.product.id)

    def test_update_product_normal_user_forbidden(self):
        url = f"{self.base_url}{self.product.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_unauthenticated(self):
        url = f"{self.base_url}{self.product.id}/update/"

        self.client.credentials()
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product_invalid_category(self):
        url = f"{self.base_url}{self.product.id}/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_not_found(self):
        url = f"{self.base_url}9999/update/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

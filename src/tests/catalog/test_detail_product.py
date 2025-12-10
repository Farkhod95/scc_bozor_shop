from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.catalog.models import Product

User = get_user_model()


class TestProductDetailAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/categories.json",
        "tests/catalog/fixtures/products.json",
    ]

    def setUp(self):
        self.user = User.objects.get(id=2)
        tokens = JWTService.create_tokens(self.user.id)
        self.access = tokens["access"]

        self.base_url = "/api/catalog/v1/product/"
        self.product = Product.objects.get(id=1)

    def test_product_detail_success(self):
        url = f"{self.base_url}{self.product.id}/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["id"], self.product.id)
        self.assertEqual(data["name"], self.product.name)

    def test_product_detail_unauthenticated(self):
        url = f"{self.base_url}{self.product.id}/detail/"

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_detail_not_found(self):
        url = f"{self.base_url}9999/detail/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

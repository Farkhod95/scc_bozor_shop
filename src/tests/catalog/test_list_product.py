from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.auth.jwt import JWTService
from apps.catalog.models import Product

User = get_user_model()


class TestProductsListAPI(APITestCase):
    fixtures = [
        "tests/catalog/fixtures/users.json",
        "tests/catalog/fixtures/categories.json",
        "tests/catalog/fixtures/products.json",
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.tokens = JWTService.create_tokens(self.user.id)
        self.access = self.tokens["access"]

        self.url = "/api/catalog/v1/product/list/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_products_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("data", data)
        self.assertIsInstance(data["data"], list)
        self.assertGreaterEqual(len(data["data"]), 1)

    def test_products_list_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

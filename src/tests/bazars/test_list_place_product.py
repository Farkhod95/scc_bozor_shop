from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import PlaceProduct, Place
from apps.catalog.models import Product

User = get_user_model()


class TestListPlaceProductAPI(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
        "tests/bazars/fixtures/places.json",
        "tests/catalog/fixtures/files.json",
        "tests/catalog/fixtures/categories.json",
        "tests/catalog/fixtures/subcategories.json",
        "tests/catalog/fixtures/products.json",
        "tests/bazars/fixtures/place_products.json",
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

        # Normal user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.place = Place.objects.get(id=1)
        self.base_url = "/api/bazars/v1/place-product/list/"

    def test_list_place_product_success_by_superadmin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertTrue(len(response.data["data"]) > 0)

        product = response.data["data"][0]
        self.assertIn("id", product)
        self.assertIn("place_id", product)
        self.assertIn("product_id", product)
        self.assertIn("price", product)
        self.assertIn("quantity", product)

    def test_list_place_product_success_by_bazar_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access}")
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_list_place_product_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_place_product_filter_by_place(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.get(self.base_url, {"place_id": self.place.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data["data"]:
            self.assertEqual(product["place_id"], self.place.id)

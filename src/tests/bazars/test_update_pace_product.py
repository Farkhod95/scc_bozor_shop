from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import PlaceProduct

User = get_user_model()


class TestUpdatePlaceProductAPI(APITestCase):
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

        self.place_product = PlaceProduct.objects.get(id=1)
        self.base_url = "/api/bazars/v1/place-product/"

        self.payload = {
            "price": "200.00",
            "quantity": 20
        }

    def test_update_place_product_success_by_superadmin(self):
        url = f"{self.base_url}{self.place_product.id}/update/"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place_product.refresh_from_db()
        self.assertEqual(str(self.place_product.price), self.payload["price"])
        self.assertEqual(self.place_product.quantity, self.payload["quantity"])

    def test_update_place_product_success_by_bazar_admin(self):
        url = f"{self.base_url}{self.place_product.id}/update/"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place_product.refresh_from_db()
        self.assertEqual(str(self.place_product.price), self.payload["price"])
        self.assertEqual(self.place_product.quantity, self.payload["quantity"])

    def test_update_place_product_not_found(self):
        url = f"{self.base_url}9999/update/"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_place_product_forbidden_for_normal_user(self):
        url = f"{self.base_url}{self.place_product.id}/update/"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_place_product_unauthenticated(self):
        url = f"{self.base_url}{self.place_product.id}/update/"
        self.client.credentials()
        response = self.client.patch(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_place_product_validation_error(self):
        url = f"{self.base_url}{self.place_product.id}/update/"
        payload = {"price": "-100", "quantity": 0}  # invalid
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

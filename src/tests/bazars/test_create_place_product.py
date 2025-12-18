from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.core.auth.jwt import JWTService
from apps.bazars.models import Place, PlaceProduct
from apps.catalog.models import Product

User = get_user_model()


class TestCreatePlaceProductAPI(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
        "tests/bazars/fixtures/bazar_admins.json",
        "tests/bazars/fixtures/places.json",
        "tests/catalog/fixtures/files.json",
        "tests/catalog/fixtures/subcategories.json",
        "tests/catalog/fixtures/categories.json",
        "tests/catalog/fixtures/products.json",
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
        self.product = Product.objects.get(id=1)
        self.base_url = "/api/bazars/v1/place-product/create/"

        self.payload = {
            "place_id": self.place.id,
            "product_id": self.product.id,
            "price": "150.00",
            "quantity": 10
        }

    def test_create_place_product_success_by_superadmin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            PlaceProduct.objects.filter(place=self.place, product=self.product).exists()
        )

    def test_create_place_product_success_by_bazar_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_access}")
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            PlaceProduct.objects.filter(place=self.place, product=self.product).exists()
        )

    def test_create_place_product_forbidden_for_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_place_product_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.base_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_place_product_place_not_found(self):
        payload = {**self.payload, "place_id": 9999}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_place_product_product_not_found(self):
        payload = {**self.payload, "product_id": 9999}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_place_product_validation_error(self):
        payload = {**self.payload, "quantity": 0}  # min_value=1
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.super_access}")
        response = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

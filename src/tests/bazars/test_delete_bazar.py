from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.bazars.models import Bazar, Place
from apps.core.auth.jwt import JWTService


class DeleteBazarTestCase(APITestCase):
    fixtures = [
        "tests/bazars/fixtures/users.json",
        "tests/bazars/fixtures/regions.json",
        "tests/bazars/fixtures/cities.json",
        "tests/bazars/fixtures/bazars.json",
    ]

    def setUp(self):
        # SuperAdmin
        self.superadmin = User.objects.get(id=1)
        tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = tokens["access"]

        # normal user
        self.normal_user = User.objects.get(id=3)
        normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = normal_tokens["access"]

        self.base_url = "/api/bazars/v1/bazar/"
        self.bazar = Bazar.objects.get(id=1)

    def test_delete_bazar_success(self):
        url = f"{self.base_url}{self.bazar.id}/delete/"

        place_ids = list(
            Place.objects.filter(bazar_id=self.bazar.id)
            .values_list("id", flat=True)
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Bazar.objects.filter(id=self.bazar.id).exists())
        self.assertFalse(Place.objects.filter(id__in=place_ids).exists())

    def test_delete_bazar_normal_user_forbidden(self):
        url = f"{self.base_url}{self.bazar.id}/delete/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_bazar_unauthenticated(self):
        url = f"{self.base_url}{self.bazar.id}/delete/"

        self.client.credentials()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_bazar_not_found(self):
        url = f"{self.base_url}9999/delete/"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestDeleteUserAPI(APITestCase):
    fixtures = [
        "tests/accounts/fixtures/users.json",
    ]

    def setUp(self):
        self.superadmin = User.objects.get(id=1)
        self.tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = self.tokens["access"]

        self.normal_user = User.objects.get(id=2)
        self.normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = self.normal_tokens["access"]

        self.user_to_delete = 3
        self.url = f"/api/accounts/v1/users/{self.user_to_delete}/delete/"

    def test_delete_user_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Confirm user is deleted
        self.assertFalse(User.objects.filter(id=self.user_to_delete).exists())

    def test_delete_user_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_not_superadmin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.delete("/api/accounts/v1/users/999/delete/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

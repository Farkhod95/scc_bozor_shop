from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestUpdateUserAPI(APITestCase):
    fixtures = [
        "tests/accounts/fixtures/users.json",
    ]

    def setUp(self):
        # SuperAdmin user
        self.superadmin = User.objects.get(id=1)
        self.tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = self.tokens["access"]

        self.normal_user = User.objects.get(id=2)
        self.normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = self.normal_tokens["access"]

        # User to update
        self.user_to_update = User.objects.get(id=3)
        self.url = f"/api/accounts/v1/users/{self.user_to_update.id}/update/"

        self.valid_payload = {
            "username": "updated_user",
            "password": "NewPassword123!",
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "+998901234568",
            "profile_image": None
        }

        self.invalid_payload = {
            "username": "",
            "password": "123"
        }

    def test_update_user_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data["message"])
        self.assertEqual(data["data"]["username"], "updated_user")

    def test_update_user_unauthenticated(self):
        self.client.credentials()
        response = self.client.patch(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_non_superadmin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.patch(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.patch(self.url, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        url = "/api/accounts/v1/users/9999/update/"
        response = self.client.patch(url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

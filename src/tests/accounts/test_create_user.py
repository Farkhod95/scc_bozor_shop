from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestCreateUserAPI(APITestCase):
    fixtures = [
        "tests/accounts/fixtures/users.json",
    ]

    def setUp(self):
        # SuperAdmin user
        self.superadmin = User.objects.get(id=1)
        self.tokens = JWTService.create_tokens(self.superadmin.id)
        self.access = self.tokens["access"]

        # Normal authenticated user
        self.normal_user = User.objects.get(id=2)
        self.normal_tokens = JWTService.create_tokens(self.normal_user.id)
        self.normal_access = self.normal_tokens["access"]
        self.url = "/api/accounts/v1/users/create/"

        self.valid_payload = {
            "username": "new_user",
            "password": "Password123!",
            "email": "new@example.com",
            "first_name": "Ali",
            "last_name": "Valiyev",
            "phone_number": "+998901234567",
            "profile_image": None
        }

        self.invalid_payload = {
            "username": "",
            "password": "123"
        }

    def test_create_user_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertTrue(data["message"])
        self.assertEqual(data["data"]["username"], "new_user")

    def test_create_user_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_non_superadmin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_access}")
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(self.url, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

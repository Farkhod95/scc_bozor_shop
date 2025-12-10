from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.auth.jwt import JWTService

User = get_user_model()


class TestUserProfileAPI(APITestCase):
    fixtures = [
        'tests/accounts/fixtures/users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.url = "/api/accounts/v1/users/me/"

        tokens = JWTService.create_tokens(self.user.id)
        access = tokens["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_user_profile_without_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["data"]['username'], self.user.username)

from rest_framework.test import APITestCase
from rest_framework import status


class TestLoginAPI(APITestCase):
    fixtures = ['tests/accounts/fixtures/users.json']

    def setUp(self):
        self.url = "/api/accounts/v1/auth/login/"

    def test_login_success(self):
        response = self.client.post(self.url, {
            "username": "superuser",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "data" in response.data
        assert "message" in response.data

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {
            "username": "superuser",
            "password": "wrongpass"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_without_username(self):
        response = self.client.post(self.url, {
            "password": "password123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_without_password(self):
        response = self.client.post(self.url, {
            "username": "superuser"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
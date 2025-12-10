from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestRegisterUserAPI(APITestCase):
    fixtures = [
        "tests/accounts/fixtures/users.json",
    ]

    def setUp(self):
        self.url = "/api/accounts/v1/auth/register/"

        self.valid_payload = {
            "username": "new_user",
            "password": "Password123!",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Valiyev",
            "phone_number": "+998901234567",
            "profile_image": None
        }

        self.invalid_payload = {
            "username": "",
            "password": "123",
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertIn("data", data)
        self.assertIn("access", data["data"])
        self.assertIn("refresh", data["data"])

        # User created
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_register_user_invalid_data(self):
        response = self.client.post(self.url, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_username_already_taken(self):
        user = User.objects.get(id=1)

        payload = {**self.valid_payload, "username": user.username}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

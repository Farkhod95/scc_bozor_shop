# Tests

## Introduction
Tests are a crucial part of any project. Without them, supporting or refactoring becomes much more difficult and error-prone. That's why I added tests in the first place—to ensure that the code remains maintainable, reliable, and easier to modify over time.


## Testing Approaches
There are many types of tests, such as unit, integration, and end-to-end (E2E) tests, as well as concepts like black-box and white-box testing. Each type has its own strengths and weaknesses, but by combining them, we can strike the right balance for effective testing

## How to write test
Django offers excellent built-in tools for testing, such as fixtures, unittest, and the request factory, which we'll use to streamline our testing process. Each test must include at least two cases—one for success and one for failure. Tests should be independent, meaning no test should rely on or call another. External resources should be mocked to isolate the functionality under test. Additionally, test code should be written in a declarative style—avoid using loops or other constructs that could make the code harder to read.

## Testing Structure Overview:

In root directory we have tests directory holds all the test-related components. Below is how the structure is organized, using the users app as an example, though this could be separated logically depending on the app or feature.

* tests/users/fixtures/: This directory contains all the data we preload into the database when running tests. Each test has its own dedicated fixtures, meaning we don’t share fixtures across test cases.

* test_user_create.py: This file contains tests for a single feature, following a rule of one feature per test file to maintain focus and clarity.

Here’s an example of how the structure looks:

```
tests
  users
    fixtures
      test_user_list
      test_user_detail
      test_user_create
        company.json
        token.json
    test_user_list.py
    test_user_detial.py
    test_user_create.py
```

Example Fixture:
```
[
  {
    "model": "app.User",
    "pk": 1,
    "fields": {
      "email": "user1@gmail.com",
      "password": "password1",
      "company": 1,
      "first_name": "User 1",
      "last_name": "Kim",
      "is_superuser": true,
      "is_active": true,
      "created_at": "2024-03-23T04:48:47.402555+00",
      "updated_at": "2024-03-23T04:48:47.402555+00"
    }
  }
]
```


Example Test:
```python
from rest_framework.test import APITestCase

class TestUserCreate(APITestCase):
    fixtures = [
        "app/tests/users/fixtures/test_user_create/company.json",
        "app/tests/users/fixtures/test_user_create/token.json",
    ]

    def test_user_create(self):
        data = {
            'first_name': "Bekhzod",
            'last_name': "Tillakhanov",
            'is_active': True,
            'email': "admin@gmail.com",
            'password': "123456",
        }

        headers = {"Authorization": "Token TDgk8ATW132ZG-DYkfCw6Hhf55715SSs56DY"}
        response = self.client.post("/api/v1/users/create/", data, headers=headers)

        self.assertEqual(response.status_code, 201, response)
        self.assertIsNotNone(response.data["id"])

        user = User.objects.filter(id=response.data["id"]).get()
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.company.id, 1)
        self.assertEqual(user.is_active, data['is_active'])
        self.assertEqual(user.email, data['email'])
```

This setup ensures tests are isolated and clear, making it easier to manage test data and functionality. Each test file focuses on a specific feature, while fixtures help keep tests independent from each other.


## Mock
Mocks allow us to test interactions with external resources or systems that are outside of our control. However, we should never use mocks to test our internal features, as they should be tested directly to ensure they work as expected under real conditions.

```python
from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase

class TestUserSignUpGoogle(APITestCase):
    fixtures = [
        "app/tests/users/fixtures/test_user_create/company.json",
        "app/tests/users/fixtures/test_user_create/token.json",
    ]

    @patch("apps.auth.services.google.requests")
    def test_user_create(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "username": "Bekhzod"}
        mock_requests.get.return_value = mock_response

        data = {
            "code": "5Tihxd2KV0VsUFE_-VD4_Sq2yAMRDNuDnMDj0cF",
        }
        response = self.client.post("/api/v1/auth/google/sign-up/", data)
        self.assertEqual(response.status_code, 201, response)
        self.assertIsNotNone(response.data["token"])
```

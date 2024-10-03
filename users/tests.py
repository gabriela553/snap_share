import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserRegistrationTests(APITestCase):
    TEST_PASSWORD = "existing_password"

    def setUp(self) -> None:
        self.existing_user = User.objects.create_user(
            username="existing_user",
            email="existing@example.com",
            password=self.TEST_PASSWORD,
        )
        self.register_url = reverse("register")

    def tearDown(self) -> None:
        self.existing_user.delete()

    def test_register_success(self) -> None:
        data = {
            "username": "new_user",
            "email": "newuser@example.com",
            "password1": "password987",
            "password2": "password987",
        }
        response = self.client.post(
            self.register_url,
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            User.objects.get(username="new_user").email,
            "newuser@example.com",
        )

    def test_register_passwords_do_not_match(self) -> None:
        data = {
            "username": "new_user",
            "email": "newuser@example.com",
            "password1": "password987",
            "password2": "password876",
        }
        response = self.client.post(
            self.register_url,
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_email_already_exists(self) -> None:
        data = {
            "username": "another_user",
            "email": "existing@example.com",
            "password1": "password987",
            "password2": "password987",
        }
        response = self.client.post(
            self.register_url,
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(
            response.data["email"][0],
            "Konto dla tego adresu email już istnieje.",
        )

    def test_register_invalid_email_format(self) -> None:
        data = {
            "username": "user_invalid_email",
            "email": "invalid-email-format",
            "password1": "password987",
            "password2": "password987",
        }
        response = self.client.post(
            self.register_url,
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class UserAuthTests(APITestCase):
    TEST_PASSWORD = "testpass"

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password=self.TEST_PASSWORD,
        )
        self.login_url = reverse("token_obtain_pair")

    def tearDown(self) -> None:
        self.user.delete()

    def test_login(self) -> None:
        data = {
            "username": "testuser",
            "password": "testpass",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

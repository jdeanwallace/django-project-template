from model_bakery import baker
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.test import TestCase
from django.conf import settings


# Create your tests here.
class AuthTokenTest(APITestCase):

    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL, email='me@example.com')
        self.user.set_password('password')
        self.user.save()
        baker.make('authtoken.Token', user=self.user)

    def test_login_missing_data(self):
        response = self.client.post(
            reverse('accounts-api:auth-token'),
            data={},
        )
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(
            response.data,
            {
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
            response.content,
        )

    def test_login_empty_data(self):
        response = self.client.post(
            reverse('accounts-api:auth-token'),
            data={"email": "", "password": ""},
        )
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(
            response.data,
            {
                "email": ["This field may not be blank."],
                "password": ["This field may not be blank."],
            },
            response.content,
        )

    def test_login_inactive_user(self):
        # Make user inactive.
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            reverse('accounts-api:auth-token'),
            data={"email": "me@example.com", "password": "password"},
        )
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(
            response.data,
            {
                "non_field_errors": ["Unable to log in with provided credentials."],
            },
            response.content,
        )

    def test_login_success(self):
        response = self.client.post(
            reverse('accounts-api:auth-token'),
            data={"email": "me@example.com", "password": "password"},
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(
            response.data,
            {"token": self.user.auth_token.key},
            response.content,
        )

    def test_login_unsupported_method(self):
        for method in ['get', 'put', 'patch']:
            with self.subTest(method=method):
                method_func = getattr(self.client, method)
                response = method_func(
                    reverse('accounts-api:auth-token'),
                    data={"email": "me@example.com", "password": "password"},
                )
                self.assertEqual(response.status_code, 405, response.content)
                self.assertEqual(
                    response.data,
                    {"detail": f"Method \"{method.upper()}\" not allowed."},
                    response.content,
                )

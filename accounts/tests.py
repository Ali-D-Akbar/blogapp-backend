import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from accounts.views import LoginAPI, RegisterAPI

pytestmark = pytest.mark.django_db


class AccountTests(APITestCase):
    """
    Tests for Accounts.
    """
    def register(self, credentials):
        """
        Registers a user given the credentials for test purposes.
        """
        factory = APIRequestFactory()
        view = RegisterAPI.as_view()
        url = '/api/auth/register'

        request = factory.post(url, credentials)
        return view(request)

    def login(self, credentials):
        """
        logs-in a user given the credentials for test purposes.
        """
        factory = APIRequestFactory()
        view = LoginAPI.as_view()
        url = '/api/auth/login'

        request = factory.post(url, credentials)
        return view(request)

    def test_register_success(self):
        """
        Tests if a user can register successfully.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }
        response = self.register(credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_register_fail(self):
        """
        Tests if a user fails to register given the bad credentials.
        """
        credentials = {
            'username': 'test',
            'password': '123'
        }
        response = self.register(credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """
        Tests if a user can login successfully.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }
        response = self.register(credentials)

        credentials = {
            'username': 'test',
            'password': '123'
        }

        response = self.login(credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_failed(self):
        """
        Tests if a user fails to login given the bad credentials.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }
        response = self.register(credentials)

        credentials = {
            'username': 'test',
            'password': '12345'
        }

        response = self.login(credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

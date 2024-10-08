from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

from profiles.models import Profile


class UserRegistrationTest(APITestCase):
    """
    Test class for '/register' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_user_registration.UserRegistrationTest
    """

    def test_user_registration(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@domain.com',
            'password1': 'super_secret_password1',
            'password2': 'super_secret_password1'
        }

        self.assertEqual(User.objects.count(), 0)  # type: ignore
        self.assertEqual(Profile.objects.count(), 0)  # type: ignore

        response = self.client.post(reverse('register'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('User registered successfully.', response.json()['detail'])
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        self.assertEqual(Profile.objects.count(), 1)  # type: ignore

    def test_user_registration_invalid_password(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@domain.com',
            'password1': 'abc',
            'password2': 'abc'
        }

        response = self.client.post(reverse('register'), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.json()['password1'])
        self.assertFalse(User.objects.filter(username=data['username']).exists())

    def test_user_registration_invalid_email(self):
        data = {
            'username': 'test_user',
            'email': 'test_user',
            'password1': 'super_secret_password1',
            'password2': 'super_secret_password1'
        }

        response = self.client.post(reverse('register'), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.json()['email'])
        self.assertFalse(User.objects.filter(username=data['username']).exists())

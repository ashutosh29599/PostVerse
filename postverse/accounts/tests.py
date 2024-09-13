from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class UserRegistrationTest(APITestCase):
    """
        make test module=postverse.accounts.tests.UserRegistrationTest
    """
    def test_user_registration(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@domain.com',
            'password1': 'super_secret_password1',
            'password2': 'super_secret_password1'
        }

        response = self.client.post(reverse('register'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('User registered successfully.', response.json()['detail'])
        self.assertTrue(User.objects.filter(username=data['username']).exists())

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


class UserLoginTokenTest(APITestCase):
    """
        make test module=postverse.accounts.tests.UserLoginTokenTest
    """

    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'password': 'super_secret_password1'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

    def test_token_generation(self):
        response = self.client.post(reverse('token_obtain_pair'), self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

    def test_token_generation_incorrect_credentials(self):
        response = self.client.post(reverse('token_obtain_pair'), data={
            'username': 'test_user',
            'password': 'incorrect_password'
        })

        self.assertIn('No active account found with the given credentials', response.json()['detail'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        refresh_token = self.client.post(reverse('token_obtain_pair'), self.user_data).json()['refresh']
        response = self.client.post(reverse('token_refresh'), {
            'refresh': refresh_token
        })

        self.assertIn('access', response.json())

    def test_token_refresh_invalid_refresh_token(self):
        response = self.client.post(reverse('token_refresh'), {
            'refresh': 'abcd'
        })

        self.assertIn('Token is invalid or expired', response.json()['detail'])


class ChangePasswordTest(APITestCase):
    """
        make test module=postverse.accounts.tests.ChangePasswordTest
    """
    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'password': 'super_secret_password1'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

        self.access_token = self.client.post(reverse('token_obtain_pair'), data=self.user_data).json()['access']

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('Password has been changed successfully.', response.json()['detail'])

        # Test if you are able to get access/refresh tokens with the new credentials.
        response = self.client.post(reverse('token_obtain_pair'), data={
            'username': self.user_data['username'],
            'password': 'new_secret_password1'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

        # Test to see that you aren't getting access/refresh tokens with the old credentials.
        response = self.client.post(reverse('token_obtain_pair'), data={
            'username': self.user_data['username'],
            'password': 'super_secret_password1'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('No active account found with the given credentials', response.json()['detail'])

    def test_change_password_incorrect_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'old_password': 'incorrect_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('Your old password is incorrect.', response.json()['old_password'])

    def test_change_password_invalid_new_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'abc',
            'new_password2': 'abc'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.json()['non_field_errors'])

    def test_change_password_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer abcd')

        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('Given token not valid for any token type', response.json()['detail'])

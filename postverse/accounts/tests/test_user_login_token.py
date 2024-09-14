from django.urls import reverse
from rest_framework import status

from .registered_users_tests_base import RegisteredUsersTestBase


class UserLoginTokenTest(RegisteredUsersTestBase):
    """
        make test module=postverse.accounts.tests.UserLoginTokenTest
    """
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

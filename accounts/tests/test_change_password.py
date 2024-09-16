from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class ChangePasswordTest(RegisteredUsersTestBase):
    """
        make test module=accounts.tests.test_change_password.ChangePasswordTest
    """

    def setUp(self):
        super().setUp()
        super().authenticate()

    def test_change_password(self):
        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('Password has been changed successfully.', response.json()['detail'])

        # Test if you are able to get access/refresh tokens with the new credentials.
        response = self.client.post(reverse('token_obtain_pair'), data={
            'username': self.user_credentials['username'],
            'password': 'new_secret_password1'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

        # Test to see that you aren't getting access/refresh tokens with the old credentials.
        response = self.client.post(reverse('token_obtain_pair'), data={
            'username': self.user_credentials['username'],
            'password': 'super_secret_password1'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('No active account found with the given credentials', response.json()['detail'])

    def test_change_password_incorrect_credentials(self):
        data = {
            'old_password': 'incorrect_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('Your old password is incorrect.', response.json()['old_password'])

    def test_change_password_invalid_new_password(self):
        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'abc',
            'new_password2': 'abc'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.json()['non_field_errors'])

    def test_change_password_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer abcd')

        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)
        self.assertIn('Given token not valid for any token type', response.json()['detail'])

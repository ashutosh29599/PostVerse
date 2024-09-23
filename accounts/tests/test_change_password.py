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

        # Test to see if you are able to login with the new credentials.
        response = self.client.post(reverse('login'), data={
            'username': self.user_credentials['username'],
            'password': data['new_password1']
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Login successful.', response.json()['detail'])
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)

        # Test to make sure you cannot login with the old credentials.
        response = self.client.post(reverse('login'), data={
            'username': self.user_credentials['username'],
            'password': data['old_password']
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('Invalid credentials', response.json()['detail'])

    def test_change_password_incorrect_credentials(self):
        data = {
            'old_password': 'incorrect_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('Your old password is incorrect.', response.json()['old_password'])

    def test_change_password_invalid_new_password(self):
        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'abc',
            'new_password2': 'abc'
        }

        response = self.client.put(reverse('change_password'), data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.json()['non_field_errors'])

    def test_change_password_invalid_access_token(self):
        super().authenticate(correct_access_token=False)

        data = {
            'old_password': 'super_secret_password1',
            'new_password1': 'new_secret_password1',
            'new_password2': 'new_secret_password1'
        }

        response = self.client.put(reverse('change_password'), data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertIn('Invalid token', response.json()['detail'])

from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserLoginTest(RegisteredUsersTestBase):
    """
    Test class for '/login' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_user_login_token.UserLoginTokenTest
    """

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('login'), data={
            'username': self.user_credentials['username'],
            'password': self.user_credentials['password1']
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Login successful', response.json()['detail'])
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)

    def test_login_with_incorrect_credentials(self):
        response = self.client.post(reverse('login'), data={
            'username': self.user_credentials['username'],
            'password': 'incorrect_password'
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('Invalid credentials', response.json()['detail'])
        self.assertNotIn('access', response.cookies)
        self.assertNotIn('refresh', response.cookies)

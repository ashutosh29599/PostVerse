from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserAuthenticationVerificationTest(RegisteredUsersTestBase):
    """
        make test module=accounts.tests.test_user_verify_authentication.UserAuthenticationVerificationTest
    """

    def setUp(self):
        super().setUp()

    def test_verify_authentication_with_correct_token(self):
        super().authenticate()

        response = self.client.get(reverse('check_auth'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Authenticated', response.json()['detail'])
        self.assertEqual(self.user_credentials['username'], response.json()['username'])

    def test_verify_authentication_with_incorrect_token(self):
        super().authenticate(correct_access_token=False)

        response = self.client.get(reverse('check_auth'))

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('Invalid token', response.json()['detail'])

from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserTokenRefreshTest(RegisteredUsersTestBase):
    """
    Test class for '/token_refresh' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_user_token_refresh.UserTokenRefreshTest
    """

    def test_token_refresh(self):
        super().authenticate()

        response = self.client.post(reverse('token_refresh'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('access', response.cookies)

    def test_token_refresh_invalid_refresh_token(self):
        super().authenticate(correct_refresh_token=False)

        response = self.client.post(reverse('token_refresh'))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('Invalid or expired refresh token', response.json()['detail'])

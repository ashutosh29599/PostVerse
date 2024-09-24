from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserLogoutTest(RegisteredUsersTestBase):
    """
    Test class for '/logout' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_user_logout.UserLogoutTest
    """

    def test_user_logout(self):
        super().authenticate()
        response = self.client.post(reverse('logout'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Successfully logged out', response.json()['detail'])
        if 'access' in response:
            self.assertEqual('', response.cookies['access'])
        if 'refresh' in response:
            self.assertEqual('', response.cookies['refresh'])

    def test_in(self):
        super().authenticate(correct_access_token=False)

        response = self.client.post(reverse('logout'))

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('Invalid token', response.json()['detail'])

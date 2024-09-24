from django.shortcuts import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserProfileFetchTest(RegisteredUsersTestBase):
    """
    Test class for '/profile' endpoint.

    Command to run the tests of this class:
        make test module=profiles.tests.test_user_profile_fetch.UserProfileFetchTest
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def test_fetch_user_profile(self):
        response = self.client.get(reverse('profile', kwargs={'username': self.user_credentials['username']}))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'user': self.user.id, 'first_name': None, 'last_name': None, 'bio': None, 'photo': None},
                         response.json())

    def test_fetch_user_profile_invalid_username(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'non_existent_username'}))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('No Profile matches the given query.', response.json()['detail'])

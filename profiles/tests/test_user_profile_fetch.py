from django.shortcuts import reverse
from rest_framework import status

from .user_profile_tests import UserProfileTest


class UserProfileFetchTest(UserProfileTest):
    """
        make test module=profiles.tests.test_user_profile.UserProfileFetchTest
    """

    def test_fetch_user_profile(self):
        response = self.client.get(reverse('profile', kwargs={'username': self.user_credentials['username']}))

        self.assertEqual({'user': self.user.id, 'first_name': None, 'last_name': None, 'bio': None, 'photo': None},
                         response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_fetch_user_profile_invalid_username(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'non_existent_username'}))

        self.assertEqual('No Profile matches the given query.', response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

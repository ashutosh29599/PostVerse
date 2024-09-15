from django.shortcuts import reverse
from rest_framework import status

from .user_profile_tests import UserProfileTest


class UserProfileUpdateTest(UserProfileTest):
    """
        make test module=profiles.tests.test_user_profile_update.UserProfileUpdateTest
    """

    def test_update_user_profile(self):
        profile_data = {
            'user': self.user.id,
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'This is the test bio!'
        }

        response = self.client.patch(reverse('edit_profile'), data=profile_data)

        self.assertEqual(
            {'user': self.user.id, 'first_name': 'Test', 'last_name': 'User', 'bio': 'This is the test bio!',
             'photo': None}, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

from django.shortcuts import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserProfileUpdateTest(RegisteredUsersTestBase):
    """
    Test class for '/edit_profile' endpoint.

    Command to run the tests of this class:
        make test module=profiles.tests.test_user_profile_update.UserProfileUpdateTest
    """

    # TODO: add photo in the tests.
    # TODO: Add test where the photo is updated.
    # TODO: Add test where the request is sent without any data.
    # TODO: Add test where the incorrect user id is sent.

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate(*args, **kwargs)

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

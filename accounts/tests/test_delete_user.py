from django.urls import reverse
from rest_framework import status

from .registered_users_tests_base import RegisteredUsersTestBase


class UserDeletionTest(RegisteredUsersTestBase):
    """
        make test module=accounts.tests.test_delete_user.UserDeletionTest
    """

    def test_delete_user(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), data=self.user_data).json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.delete(reverse('delete_user'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserDeletionTest(RegisteredUsersTestBase):
    """
        make test module=accounts.tests.test_delete_user.UserDeletionTest
    """

    def setUp(self):
        super().setUp()
        super().authenticate()

    def test_delete_user(self):
        response = self.client.delete(reverse('delete_user'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

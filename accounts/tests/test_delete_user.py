from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserDeletionTest(RegisteredUsersTestBase):
    """
    Test class for '/delete_user' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_delete_user.UserDeletionTest
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def test_delete_user(self):
        response = self.client.delete(reverse('delete_user'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

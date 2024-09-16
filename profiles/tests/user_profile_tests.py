from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserProfileTest(RegisteredUsersTestBase):
    def setUp(self):
        super().setUp()
        super().authenticate()

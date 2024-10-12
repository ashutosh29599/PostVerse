from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils.UserFactory import create_user
from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserFetchingTest(APITestCase):
    """
    Test class for '/accounts/' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_user_fetch.UserFetchingTest
    """

    def setUp(self):
        self.user1_credentials, self.user1 = create_user(self.client, username='test_user',
                                                         email='test_user@domain.com')
        self.user2_credentials, self.user2 = create_user(self.client, username='test_user_2',
                                                         email='test_user_2@domain.com')

    def test_fetch_all_users_default_settings(self):
        response = self.client.get(reverse('user-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])
        self.assertEqual('test_user_2', response.json()[1]['username'])
        self.assertEqual('test_user_2@domain.com', response.json()[1]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_all_users_with_all_data_by_flagging_true_manually(self):
        response = self.client.get(reverse('user-list'), data={
            'email': 'true',
            'date_joined': 'true',
            'first_name': 'True',
            'last_name': 'TRUE',
            'photo': 'true',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_all_users_with_all_data_by_flagging_all_flag_to_true(self):
        response = self.client.get(reverse('user-list'), data={
            'all': 'true'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_all_users_deny_all_data_that_can_be_denied(self):
        response = self.client.get(reverse('user-list'), data={
            'email': 'false',
            'date_joined': 'false',
            'first_name': 'False',
            'last_name': 'FALSE',
            'photo': 'false',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertIn('username', response.json()[0])
        self.assertNotIn('email', response.json()[0])
        self.assertNotIn('date_joined', response.json()[0])
        self.assertNotIn('first_name', response.json()[0])
        self.assertNotIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_a_single_user_default_settings(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_a_single_user_with_all_data_by_flagging_true_manually(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'email': 'true',
            'date_joined': 'true',
            'first_name': 'True',
            'last_name': 'TRUE',
            'photo': 'true',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_a_single_user_with_all_data_by_flagging_all_flag_to_true(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'all': 'true'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_a_single_user_deny_all_data_that_can_be_denied(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'email': 'false',
            'date_joined': 'false',
            'first_name': 'False',
            'last_name': 'FALSE',
            'photo': 'false',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])

        self.assertIn('username', response.json()[0])
        self.assertNotIn('email', response.json()[0])
        self.assertNotIn('date_joined', response.json()[0])
        self.assertNotIn('first_name', response.json()[0])
        self.assertNotIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_all_users_with_similar_username_to_query_username_default_settings(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'similar': 'true'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])
        self.assertEqual('test_user_2', response.json()[1]['username'])
        self.assertEqual('test_user_2@domain.com', response.json()[1]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_all_users_with_similar_username_to_query_username_with_all_data_by_flagging_true_manually(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'similar': 'true',
            'email': 'true',
            'date_joined': 'true',
            'first_name': 'True',
            'last_name': 'TRUE',
            'photo': 'true',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])
        self.assertEqual('test_user_2', response.json()[1]['username'])
        self.assertEqual('test_user_2@domain.com', response.json()[1]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_all_users_with_similar_username_to_query_username_with_all_data_by_flagging_all_flag_to_true(self):
        response = self.client.get(reverse('user-list'), data={
            'all': 'true'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])
        self.assertEqual('test_user_2', response.json()[1]['username'])
        self.assertEqual('test_user_2@domain.com', response.json()[1]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_all_users_with_similar_username_to_query_username_deny_all_data_that_can_be_denied(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'similar': 'true',
            'email': 'false',
            'date_joined': 'false',
            'first_name': 'False',
            'last_name': 'FALSE',
            'photo': 'false',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user_2', response.json()[1]['username'])

        self.assertIn('username', response.json()[0])
        self.assertNotIn('email', response.json()[0])
        self.assertNotIn('date_joined', response.json()[0])
        self.assertNotIn('first_name', response.json()[0])
        self.assertNotIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_a_single_user_with_username_with_incorrect_case(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'teSt_User',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user@domain.com', response.json()[0]['email'])

        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('date_joined', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])


# class SortedUserFetchingTest(UserFetchingTest):
class SortedUserFetchingTest(RegisteredUsersTestBase):
    """
        Test class for '/accounts/' endpoint, with sorted result.

        Command to run the tests of this class:
            make test module=accounts.tests.test_user_fetch.UserFetchingTest
        """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate(*args, **kwargs)
        super().update_user_profile(first_name='Test1', last_name='User1', bio='Test Bio 1')

        super().setUp(username='test_user_2', email='test_user_2@domain.com')
        super().authenticate(*args, **kwargs)
        super().update_user_profile(first_name='Test2', last_name='User2', bio='Test Bio 2')

    def test_fetch_all_users_sorted_by_username_ascending(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'username_asc'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user_2', response.json()[1]['username'])

    def test_fetch_all_users_sorted_by_username_descending(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'username_desc'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[1]['username'])
        self.assertEqual('test_user_2', response.json()[0]['username'])

    def test_fetch_all_users_sorted_by_oldest_user_accounts_first(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'oldest_first'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[0]['username'])
        self.assertEqual('test_user_2', response.json()[1]['username'])

    def test_fetch_all_users_sorted_by_newest_user_accounts_first(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'newest_first'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('test_user', response.json()[1]['username'])
        self.assertEqual('test_user_2', response.json()[0]['username'])

    def test_fetch_all_users_sorted_by_first_name_ascending(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'first_name_asc'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('Test1', response.json()[0]['first_name'])
        self.assertEqual('Test2', response.json()[1]['first_name'])

    def test_fetch_all_users_sorted_by_first_name_descending(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'first_name_desc'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('Test1', response.json()[1]['first_name'])
        self.assertEqual('Test2', response.json()[0]['first_name'])

    def test_fetch_all_users_sorted_by_last_name_ascending(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'last_name_asc'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('User1', response.json()[0]['last_name'])
        self.assertEqual('User2', response.json()[1]['last_name'])

    def test_fetch_all_users_sorted_by_last_name_descending(self):
        response = self.client.get(reverse('user-list'), data={
            'sort-by': 'last_name_desc'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))

        self.assertEqual('User1', response.json()[1]['last_name'])
        self.assertEqual('User2', response.json()[0]['last_name'])

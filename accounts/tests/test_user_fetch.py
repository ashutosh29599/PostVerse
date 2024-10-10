from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils.create_user import create_user


class UserFetchingTest(APITestCase):
    """
    Test class for '/accounts/' endpoint.

    Command to run the tests of this class:
        make test module=accounts.tests.test_user_fetch
    """

    def setUp(self):
        self.user1 = create_user(self.client, username='test_user', email='test_user@domain.com')
        self.user2 = create_user(self.client, username='test_user_2', email='test_user_2@domain.com')

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
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_all_users_with_all_data(self):
        response = self.client.get(reverse('user-list'), data={
            'email': 'true',
            'first_name': 'True',
            'last_name': 'TRUE',
            'photo': 'true',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertIn('username', response.json()[0])
        self.assertIn('email', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_all_users_without_only_default_data(self):
        response = self.client.get(reverse('user-list'), data={
            'email': 'false',
            'first_name': 'False',
            'last_name': 'FALSE',
            'photo': 'false',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertIn('username', response.json()[0])
        self.assertNotIn('email', response.json()[0])
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
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])

    def test_fetch_a_single_user_with_all_data(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'email': 'true',
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
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('photo', response.json()[0])

    def test_fetch_a_single_user_without_only_default_data(self):
        response = self.client.get(reverse('user-list'), data={
            'username': 'test_user',
            'email': 'false',
            'first_name': 'False',
            'last_name': 'FALSE',
            'photo': 'false',
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('test_user', response.json()[0]['username'])

        self.assertIn('username', response.json()[0])
        self.assertNotIn('email', response.json()[0])
        self.assertNotIn('first_name', response.json()[0])
        self.assertNotIn('last_name', response.json()[0])
        self.assertNotIn('photo', response.json()[0])


from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class UserLoginTokenTest(RegisteredUsersTestBase):
    """
        make test module=accounts.tests.test_user_login_token.UserLoginTokenTest

        TODO: we are now using LoginUserAPIView for logging the user in, not /token and /token/refresh,
        TODO: although those endpoints are still valid, so add tests for LoginUserAPIView
    """

    def test_token_generation(self):
        """
            To be deprecated with /token
        """
        response = self.client.post(reverse('token_obtain_pair'),
                                    data={
                                        'username': self.user_credentials['username'],
                                        'password': self.user_credentials['password1']
                                    })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

    def test_token_generation_incorrect_credentials(self):
        """
            To be deprecated with /token
        """
        response = self.client.post(reverse('token_obtain_pair'), data={
            'username': 'test_user',
            'password': 'incorrect_password'
        })

        self.assertIn('No active account found with the given credentials', response.json()['detail'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        super().authenticate()
        response = self.client.post(reverse('token_refresh'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.cookies)

    def test_token_refresh_invalid_refresh_token(self):
        super().authenticate(correct_refresh_token=False)
        response = self.client.post(reverse('token_refresh'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid or expired refresh token', response.json()['detail'])

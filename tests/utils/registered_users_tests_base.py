from django.contrib.auth.models import User
from django.shortcuts import reverse
from http.cookies import SimpleCookie
from rest_framework.test import APITestCase


class RegisteredUsersTestBase(APITestCase):
    def setUp(self, username='test_user', email='test_user@domain.com',
              password1='super_secret_password1', password2='super_secret_password1'):
        """
        Creates a user by calling the '/register' endpoint.

        Parameters
        __________
        username : str
        email : str
        password1 : str
        password2 : str
        """

        self.user_credentials = {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2
        }

        self.client.post(reverse('register'), self.user_credentials)
        self.user = User.objects.get(username=self.user_credentials['username'])

    def authenticate(self, correct_access_token=True, correct_refresh_token=True):
        """
        Sets access and refresh tokens as HttpOnly cookies.

        Parameters
        __________
        correct_access_token : bool
            Specifies whether the access token being set is supposed to be the correct one. True by default.
        correct_refresh_token : bool
            Specifies whether the refresh token being set is supposed to be the correct one. True by default.
        """

        tokens = self.client.post(reverse('login'), data={
            'username': self.user_credentials['username'],
            'password': self.user_credentials['password1']
        })

        self.client.cookies = SimpleCookie()

        if correct_access_token:
            self.client.cookies['access'] = tokens.cookies['access'].value
        else:
            self.client.cookies['access'] = 'abcd'

        if correct_refresh_token:
            self.client.cookies['refresh'] = tokens.cookies['refresh'].value
        else:
            self.client.cookies['refresh'] = 'wxyz'

        self.client.cookies['access']['httponly'] = True
        self.client.cookies['access']['secure'] = True

        self.client.cookies['refresh']['httponly'] = True
        self.client.cookies['refresh']['secure'] = True

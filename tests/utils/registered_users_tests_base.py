from django.contrib.auth.models import User
from django.shortcuts import reverse
from http.cookies import SimpleCookie
from rest_framework.test import APITestCase


class RegisteredUsersTestBase(APITestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'test_user',
            'email': 'test_user@domain.com',
            'password1': 'super_secret_password1',
            'password2': 'super_secret_password1'
        }

        self.client.post(reverse('register'), self.user_credentials)
        self.user = User.objects.get(username=self.user_credentials['username'])

    def authenticate(self, correct_access_token=True, correct_refresh_token=True):
        """
            Sets access and refresh tokens as HttpOnly cookies.
        """

        tokens = self.client.post(reverse('token_obtain_pair'),
                                  data={
                                      'username': self.user_credentials['username'],
                                      'password': self.user_credentials['password1']
                                  }).json()

        self.client.cookies = SimpleCookie()

        if correct_access_token:
            self.client.cookies['access'] = tokens['access']
        else:
            self.client.cookies['access'] = 'abcd'

        if correct_refresh_token:
            self.client.cookies['refresh'] = tokens['refresh']
        else:
            self.client.cookies['refresh'] = 'wxyz'

        self.client.cookies['access']['httponly'] = True
        self.client.cookies['access']['secure'] = True

        self.client.cookies['refresh']['httponly'] = True
        self.client.cookies['refresh']['secure'] = True

    # def set_access_token_as_http_only_cookie(self, correct_token=True):
    #     # Set HTTP-only cookies
    #     if correct_token:
    #         self.client.cookies = SimpleCookie({
    #             'access': self.access_token
    #         })
    #     else:
    #         self.client.cookies = SimpleCookie({
    #             'access': 'abcd'
    #         })
    #
    #     # Mark the cookie as HTTP-only
    #     self.client.cookies['access']['httponly'] = True

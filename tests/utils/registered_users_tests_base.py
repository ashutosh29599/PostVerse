from django.shortcuts import reverse
from http.cookies import SimpleCookie
from rest_framework.test import APITestCase

from tests.utils.UserFactory import create_user
from tests.utils.ProfileFactory import generate_profile_data


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

        self.user_credentials, self.user = create_user(self.client,
                                                       username=username,
                                                       email=email,
                                                       password1=password1,
                                                       password2=password2)

    def authenticate(self, user_credentials=None, correct_access_token=True, correct_refresh_token=True):
        """
        Sets access and refresh tokens as HttpOnly cookies.

        Parameters
        __________
        correct_access_token : bool
            Specifies whether the access token being set is supposed to be the correct one. True by default.
        correct_refresh_token : bool
            Specifies whether the refresh token being set is supposed to be the correct one. True by default.
        """

        if not user_credentials:
            user_credentials = self.user_credentials

        tokens = self.client.post(reverse('login'), data={
            'username': user_credentials['username'],
            'password': user_credentials['password1']
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

    def update_user_profile(self, first_name='Test', last_name='User', bio='Test Bio!', photo=None):
        """
        Updates the user profile with the given data.

        Parameters
        __________
        first_name : str
        last_name : str
        bio : str
        photo : str
            Provides the name of the photo (must be in .png format)
        """
        profile_data = generate_profile_data(self.user.id, first_name=first_name, last_name=last_name, bio=bio,
                                             photo=photo)
        self.client.patch(reverse('edit_profile'), data=profile_data)

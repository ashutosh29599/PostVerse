from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework.test import APITestCase


class UserProfileTest(APITestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'test_user',
            'email': 'test_user@domain.com',
            'password1': 'super_secret_password1',
            'password2': 'super_secret_password1'
        }

        self.client.post(reverse('register'), self.user_credentials)
        self.user = User.objects.get(username=self.user_credentials['username'])

        self.access_token = self.client.post(reverse('token_obtain_pair'),
                                             data={
                                                 'username': self.user_credentials['username'],
                                                 'password': self.user_credentials['password1']
                                             }).json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

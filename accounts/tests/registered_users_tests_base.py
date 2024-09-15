from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisteredUsersTestBase(APITestCase):
    # TODO: Create users dynamically instead of creating manually.
    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'password': 'super_secret_password1'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

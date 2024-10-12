from django.contrib.auth.models import User
from django.shortcuts import reverse


def create_user(client, username='test_user', email='test_user@domain.com',
                password1='super_secret_password1', password2='super_secret_password1'):
    user_credentials = {
        'username': username,
        'email': email,
        'password1': password1,
        'password2': password2
    }

    client.post(reverse('register'), user_credentials)
    return user_credentials, User.objects.get(username=user_credentials['username'])

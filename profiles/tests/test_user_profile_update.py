from django.shortcuts import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from profiles.tests.utils.generate_profile_data import generate_profile_data


class UserProfileUpdateTest(RegisteredUsersTestBase):
    """
    Test class for '/edit_profile' endpoint.

    Command to run the tests of this class:
        make test module=profiles.tests.test_user_profile_update.UserProfileUpdateTest
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate(*args, **kwargs)

    def test_update_user_profile_without_photo(self):
        profile_data = generate_profile_data(user_id=self.user.id, photo=None)

        response = self.client.patch(reverse('edit_profile'), data=profile_data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(profile_data['user'], response.json()['user'])
        self.assertEqual(profile_data['first_name'], response.json()['first_name'])
        self.assertEqual(profile_data['last_name'], response.json()['last_name'])
        self.assertEqual(profile_data['bio'], response.json()['bio'])
        self.assertIsNone(response.json()['photo'])

    def test_update_user_profile_with_photo(self):
        profile_data = generate_profile_data(user_id=self.user.id, photo='unit_test_image')

        response = self.client.patch(reverse('edit_profile'), data=profile_data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(profile_data['user'], response.json()['user'])
        self.assertEqual(profile_data['first_name'], response.json()['first_name'])
        self.assertEqual(profile_data['last_name'], response.json()['last_name'])
        self.assertEqual(profile_data['bio'], response.json()['bio'])
        self.assertIn('unit_test_image', response.json()['photo'])

    def test_update_user_profile_with_updated_data_and_photo(self):
        profile_data = generate_profile_data(user_id=self.user.id, photo='unit_test_image')
        response = self.client.patch(reverse('edit_profile'), data=profile_data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(profile_data['user'], response.json()['user'])
        self.assertEqual(profile_data['first_name'], response.json()['first_name'])
        self.assertEqual(profile_data['last_name'], response.json()['last_name'])
        self.assertEqual(profile_data['bio'], response.json()['bio'])
        self.assertIn('unit_test_image', response.json()['photo'])

        profile_data = generate_profile_data(user_id=self.user.id,
                                             first_name='UpdatedTest',
                                             last_name='UpdatedUser',
                                             bio='This is the updated test bio!',
                                             photo='unit_test_image2')

        response = self.client.patch(reverse('edit_profile'), data=profile_data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(profile_data['user'], response.json()['user'])
        self.assertEqual(profile_data['first_name'], response.json()['first_name'])
        self.assertEqual(profile_data['last_name'], response.json()['last_name'])
        self.assertEqual(profile_data['bio'], response.json()['bio'])
        self.assertIn('unit_test_image2', response.json()['photo'])

    def test_update_user_profile_send_no_data_on_second_update(self):
        profile_data = generate_profile_data(user_id=self.user.id, photo='unit_test_image')

        response = self.client.patch(reverse('edit_profile'), data=profile_data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(profile_data['user'], response.json()['user'])
        self.assertEqual(profile_data['first_name'], response.json()['first_name'])
        self.assertEqual(profile_data['last_name'], response.json()['last_name'])
        self.assertEqual(profile_data['bio'], response.json()['bio'])
        self.assertIn('unit_test_image', response.json()['photo'])

        response = self.client.patch(reverse('edit_profile'), data={'user': profile_data['user']})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(profile_data['user'], response.json()['user'])
        self.assertEqual(profile_data['first_name'], response.json()['first_name'])
        self.assertEqual(profile_data['last_name'], response.json()['last_name'])
        self.assertEqual(profile_data['bio'], response.json()['bio'])
        self.assertIn('unit_test_image', response.json()['photo'])

    def test_update_user_profile_without_providing_user_id(self):
        response = self.client.patch(reverse('edit_profile'), data={})

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('No Profile matches the given query.', response.json()['detail'])

    def test_update_user_profile_without_any_data(self):
        response = self.client.patch(reverse('edit_profile'), data={'user': self.user.id})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertIsNone(response.json()['first_name'])
        self.assertIsNone(response.json()['last_name'])
        self.assertIsNone(response.json()['bio'])
        self.assertIsNone(response.json()['photo'])

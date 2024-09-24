from django.shortcuts import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from posts.tests.utils.generate_post_data import generate_post_data


# def create_a_post(client, text=None, photo=None):
#     data = generate_post_data(text=text, photo=photo)
#
#     return client.post(reverse('post-list'), data=data, format='multipart')


class EditPostTest(RegisteredUsersTestBase):
    """
    Test class for POST request to '/post-detail' endpoint.

    Command to run the tests of this class:
        make test module=posts.tests.test_posts_edit.EditPostTest
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def test_edit_post_with_text_alone(self):
        data = generate_post_data(text='This is a test post!', photo=None)

        response = self.client.post(reverse('post-list'), data=data)
        post_id, post_user = response.json()['id'], response.json()['user']
        # response = create_a_post(self.client, text='This is a test post!', photo=None)
        # post_id, post_user = response.json()['id'], response.json()['user']

        data['text'] = 'This is the edited post!'
        # data = {
        #     'text': 'This is the edited post!'
        # }

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_photo_alone(self):
        photo = 'unit_test_image'
        data = generate_post_data(text=None, photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')
        post_id, post_user = response.json()['id'], response.json()['user']

        photo = 'unit_test_image2'
        data = generate_post_data(text=None, photo=photo)

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn(photo, response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_both(self):
        photo = 'unit_test_image'
        data = generate_post_data(text='This is a test post!', photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')
        post_id, post_user = response.json()['id'], response.json()['user']

        photo = 'unit_test_image2'
        data = generate_post_data(text='This is the edited post!', photo=photo)

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_text_only(self):
        photo = 'unit_test_image'
        data = generate_post_data(text='This is a test post!', photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')
        post_id, post_user = response.json()['id'], response.json()['user']

        data = {
            "text": "This is the edited post!"
        }
        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertIn('unit_test_image', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_photo_only(self):
        photo = 'unit_test_image'
        data = generate_post_data(text='This is a test post!', photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')
        post_id, post_user = response.json()['id'], response.json()['user']

        photo = 'unit_test_image2'
        data = generate_post_data(text=None, photo=photo)

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is a test post!', response.json()['text'])
        self.assertIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_neither(self):
        photo = 'unit_test_image'
        data = generate_post_data(text='This is a test post!', photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')
        post_id, post_user = response.json()['id'], response.json()['user']

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data={}, format='multipart')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('A post must either have text or photo or both.', response.json()['detail'])

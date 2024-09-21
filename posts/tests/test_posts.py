from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase


class CreatePostTest(RegisteredUsersTestBase):
    """
        make test module=posts.tests.test_posts.CreatePostTest
    """

    def setUp(self):
        super().setUp()
        super().authenticate()

    def test_create_a_post_with_text_only(self):
        data = {
            "text": "This is a test post!"
        }
        response = self.client.post(reverse('post-list'), data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertEqual(data['text'], response.json()['text'])
        self.assertIsNone(response.json()['photo'])

    def test_create_a_post_with_photo_only(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertIsNone(response.json()['text'])
        self.assertIn('unit_test_image', response.json()['photo'])

    def test_create_a_post_with_text_and_photo(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "text": "This is a test post!",
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertEqual('This is a test post!', response.json()['text'])
        self.assertIn('unit_test_image', response.json()['photo'])

    def test_create_a_post_without_text_or_photo(self):
        response = self.client.post(reverse('post-list'), data={})

        self.assertEqual('A post must either have text or photo or both.', response.json()['detail'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class EditPostTest(RegisteredUsersTestBase):
    """
        make test module=posts.tests.test_posts.EditPostTest
    """

    def setUp(self):
        super().setUp()
        super().authenticate()

    # def post_a_post(self, text=None, photo_name=None, photo_url=None):
    #     data = {}
    #
    #     if text:
    #         data['text'] = text
    #
    #     if photo_name and photo_url:
    #         with open(photo_url, 'rb') as image:
    #             data['photo'] = SimpleUploadedFile(
    #                 name=photo_name,
    #                 content=image.read(),
    #                 content_type='image/png'
    #             )
    #             return self.client.post(reverse('post-list'), data=data, format='multipart')
    #
    #     return self.client.post(reverse('post-list'), data=data)

    def test_edit_post_with_text_alone(self):
        data = {
            'text': 'This is a test post!'
        }
        response = self.client.post(reverse('post-list'), data=data)
        post_id, post_user = response.json()['id'], response.json()['user']

        data['text'] = 'This is the edited post!'

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_photo_alone(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')
            post_id, post_user = response.json()['id'], response.json()['user']

        with open('posts/tests/images/unit_test_image2.png', 'rb') as image:
            data = {
                "photo": SimpleUploadedFile(
                    name='unit_test_image2.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_both(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "text": "This is a test post!",
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')
            post_id, post_user = response.json()['id'], response.json()['user']

        with open('posts/tests/images/unit_test_image2.png', 'rb') as image:
            data = {
                "text": "This is the edited post!",
                "photo": SimpleUploadedFile(
                    name='unit_test_image2.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_text_only(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "text": "This is a test post!",
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')
            post_id, post_user = response.json()['id'], response.json()['user']

        data = {
            "text": "This is the edited post!"
        }
        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertIn('unit_test_image', response.json()['photo'])
        self.assertNotIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_photo_only(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "text": "This is a test post!",
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')
            post_id, post_user = response.json()['id'], response.json()['user']

        with open('posts/tests/images/unit_test_image2.png', 'rb') as image:
            data = {
                "photo": SimpleUploadedFile(
                    name='unit_test_image2.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data=data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is a test post!', response.json()['text'])
        self.assertIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_neither(self):
        with open('posts/tests/images/unit_test_image.png', 'rb') as image:
            data = {
                "text": "This is a test post!",
                "photo": SimpleUploadedFile(
                    name='unit_test_image.png',
                    content=image.read(),
                    content_type='image/png')
            }
            response = self.client.post(reverse('post-list'), data=data, format='multipart')
            post_id, post_user = response.json()['id'], response.json()['user']

        response = self.client.patch(reverse('post-detail', kwargs={'pk': post_id}), data={}, format='multipart')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('A post must either have text or photo or both.', response.json()['detail'])

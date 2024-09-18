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
        with open('posts/tests/unit_test_image.png', 'rb') as image:
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
        with open('posts/tests/unit_test_image.png', 'rb') as image:
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

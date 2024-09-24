from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from posts.tests.utils.PostFactory import PostFactory


class CreatePostTest(RegisteredUsersTestBase):
    """
    Test class for POST request to '/post-list' endpoint.

    Command to run the tests of this class:
        make test module=posts.tests.test_posts_create.CreatePostTest
    """

    """
        self.assertEqual(1, response.json()['count'])
        self.assertEqual(post_id, response.json()['results'][0]['id'])
        self.assertEqual(post_user, response.json()['results'][0]['user'])
        self.assertEqual('This is a test post!', response.json()['results'][0]['text'])
        self.assertIn('unit_test_image', response.json()['results'][0]['photo'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def test_create_a_post_with_text_only(self):
        data = PostFactory.generate_post_data(text='This is a test post!', photo=None)

        response = self.client.post(reverse('post-list'), data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertEqual(data['text'], response.json()['text'])
        self.assertIsNone(response.json()['photo'])

        response = self.client.get(reverse('post-list'))

        self.assertEqual(1, response.json()['count'])
        self.assertEqual(self.user.id, response.json()['results'][0]['user'])
        self.assertEqual('This is a test post!', response.json()['results'][0]['text'])
        self.assertIsNone(response.json()['results'][0]['photo'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_a_post_with_photo_only(self):
        photo = 'unit_test_image'
        data = PostFactory.generate_post_data(text=None, photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertIsNone(response.json()['text'])
        self.assertIn(photo, response.json()['photo'])

        response = self.client.get(reverse('post-list'))

        self.assertEqual(1, response.json()['count'])
        self.assertEqual(self.user.id, response.json()['results'][0]['user'])
        self.assertIsNone(response.json()['results'][0]['text'])
        self.assertIn(photo, response.json()['results'][0]['photo'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_a_post_with_text_and_photo(self):
        photo = 'unit_test_image'
        data = PostFactory.generate_post_data(text='This is a test post!', photo=photo)

        response = self.client.post(reverse('post-list'), data=data, format='multipart')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.json()['user'])
        self.assertEqual(data['text'], response.json()['text'])
        self.assertIn(photo, response.json()['photo'])

        response = self.client.get(reverse('post-list'))

        self.assertEqual(1, response.json()['count'])
        self.assertEqual(self.user.id, response.json()['results'][0]['user'])
        self.assertEqual('This is a test post!', response.json()['results'][0]['text'])
        self.assertIn(photo, response.json()['results'][0]['photo'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_a_post_without_text_or_photo(self):
        response = self.client.post(reverse('post-list'), data={})

        self.assertEqual('A post must either have text or photo or both', response.json()['detail'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

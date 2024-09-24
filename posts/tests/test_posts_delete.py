from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from posts.tests.utils.PostFactory import PostFactory


class DeletePostTest(RegisteredUsersTestBase):
    """
    Test class for DELETE request to '/post-detail' endpoint.

    Command to run the tests of this class:
        make test module=posts.tests.test_posts_delete.DeletePostTest
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def test_delete_a_post(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        response = self.client.get(reverse('post-list'))
        self.assertEqual(1, response.json()['count'])

        response = self.client.delete(reverse('post-detail', kwargs={'pk': post_id}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(reverse('post-list'))
        self.assertEqual(0, response.json()['count'])

    def test_delete_a_post_with_text_only(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo=None)
        post_id, post_user = post.json()['id'], post.json()['user']

        response = self.client.get(reverse('post-list'))
        self.assertEqual(1, response.json()['count'])

        response = self.client.delete(reverse('post-detail', kwargs={'pk': post_id}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(reverse('post-list'))
        self.assertEqual(0, response.json()['count'])

    def test_delete_a_post_with_photo_only(self):
        post = PostFactory.create_a_post(client=self.client, text=None, photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        response = self.client.get(reverse('post-list'))
        self.assertEqual(1, response.json()['count'])

        response = self.client.delete(reverse('post-detail', kwargs={'pk': post_id}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(reverse('post-list'))
        self.assertEqual(0, response.json()['count'])

    def test_delete_an_already_deleted_post(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        response = self.client.get(reverse('post-list'))
        self.assertEqual(1, response.json()['count'])

        response = self.client.delete(reverse('post-detail', kwargs={'pk': post_id}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(reverse('post-list'))
        self.assertEqual(0, response.json()['count'])

        response = self.client.delete(reverse('post-detail', kwargs={'pk': post_id}))
        self.assertEqual('No Post matches the given query.', response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

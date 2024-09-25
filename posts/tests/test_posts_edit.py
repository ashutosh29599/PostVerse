from django.shortcuts import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from posts.tests.utils.PostFactory import PostFactory


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
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo=None)
        post_id, post_user = post.json()['id'], post.json()['user']

        response = PostFactory.update_a_post(client=self.client, post_id=post_id, text='This is the edited post!')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_photo_alone(self):
        post = PostFactory.create_a_post(client=self.client, text=None, photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        photo = 'unit_test_image2'
        response = PostFactory.update_a_post(client=self.client, post_id=post_id, text=None, photo=photo)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn(photo, response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_both(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        photo = 'unit_test_image2'
        response = PostFactory.update_a_post(client=self.client, post_id=post_id,
                                             text='This is the edited post!', photo=photo)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertIn(photo, response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_text_only(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        response = PostFactory.update_a_post(client=self.client, post_id=post_id,
                                             text='This is the edited post!', photo=None)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is the edited post!', response.json()['text'])
        self.assertIn('unit_test_image', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_photo_only(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')
        post_id, post_user = post.json()['id'], post.json()['user']

        photo = 'unit_test_image2'
        response = PostFactory.update_a_post(client=self.client, post_id=post_id, text=None, photo=photo)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('This is a test post!', response.json()['text'])
        self.assertIn('unit_test_image2', response.json()['photo'])
        self.assertEqual(post_id, response.json()['id'])
        self.assertEqual(post_user, response.json()['user'])
        self.assertNotEqual(response.json()['created_at'], response.json()['updated_at'])

    def test_edit_post_with_both_text_and_photo_edit_neither(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')
        post_id = post.json()['id']

        response = PostFactory.update_a_post(client=self.client, post_id=post_id, text=None, photo=None)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('A post must either have text or photo or both.', response.json()['detail'])

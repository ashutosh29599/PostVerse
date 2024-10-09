from django.urls import reverse
from rest_framework import status

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from posts.tests.utils.PostFactory import PostFactory


class FetchPostTest(RegisteredUsersTestBase):
    """
    Test class for GET request to '/post-list' endpoint.

    Command to run the tests of this class:
        make test module=posts.tests.test_posts_fetch.FetchPostTest
    """

    # TODO: update tests to verify the username.
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def create_two_posts_from_two_different_users_and_switch_user(self):
        PostFactory.create_a_post(client=self.client, text='This is the test post by the first user!',
                                  photo='unit_test_image')

        # create another user and create a post with that user.
        super().setUp(username='test_user2', email='test_user2@domain.com')
        super().authenticate()
        PostFactory.create_a_post(client=self.client, text='This is the test post by the second user!',
                                  photo='unit_test_image2')

    def test_fetch_posts_no_posts_exist(self):
        response = self.client.get(reverse('post-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, response.json()['count'])

    def test_fetch_posts_one_post_exists(self):
        PostFactory.create_a_post(client=self.client, text='This is a test post!', photo='unit_test_image')

        response = self.client.get(reverse('post-list'))
        post = response.json()['results'][0]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, response.json()['count'])
        self.assertEqual(self.user.id, post['user'])
        self.assertEqual('This is a test post!', post['text'])
        self.assertIn('unit_test_image', post['photo'])

    def test_fetch_posts_multiple_posts_exist(self):
        PostFactory.create_a_post(client=self.client, text='This is the first test post!', photo='unit_test_image')
        PostFactory.create_a_post(client=self.client, text='This is the second test post!', photo='unit_test_image2')
        PostFactory.create_a_post(client=self.client, text='This is the third test post!', photo='unit_test_image')

        response = self.client.get(reverse('post-list'))
        posts = response.json()['results']

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.json()['count'])

        # The posts returned are, by default, ordered by creation date, with the latest posts first.
        self.assertEqual(self.user.id, posts[0]['user'])
        self.assertEqual('This is the third test post!', posts[0]['text'])
        self.assertIn('unit_test_image', posts[0]['photo'])

        self.assertEqual(self.user.id, posts[1]['user'])
        self.assertEqual('This is the second test post!', posts[1]['text'])
        self.assertIn('unit_test_image2', posts[1]['photo'])

        self.assertEqual(self.user.id, posts[2]['user'])
        self.assertEqual('This is the first test post!', posts[2]['text'])
        self.assertIn('unit_test_image', posts[2]['photo'])

    def test_fetch_posts_multiple_posts_by_multiple_users(self):
        first_user_id = self.user.id
        self.create_two_posts_from_two_different_users_and_switch_user()

        response = self.client.get(reverse('post-list'))
        posts = response.json()['results']

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, response.json()['count'])

        self.assertEqual(self.user.id, posts[0]['user'])
        self.assertEqual('This is the test post by the second user!', posts[0]['text'])
        self.assertIn('unit_test_image2', posts[0]['photo'])

        self.assertEqual(first_user_id, posts[1]['user'])
        self.assertEqual('This is the test post by the first user!', posts[1]['text'])
        self.assertIn('unit_test_image', posts[1]['photo'])

    def test_fetch_posts_by_username(self):
        first_user_id = self.user.id

        self.create_two_posts_from_two_different_users_and_switch_user()

        response = self.client.get(reverse('post-list'), data={'username': 'test_user'})
        post = response.json()['results'][0]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, response.json()['count'])

        self.assertEqual(first_user_id, post['user'])
        self.assertEqual('This is the test post by the first user!', post['text'])
        self.assertIn('unit_test_image', post['photo'])

    def test_fetch_posts_fetch_multiple_posts_by_username(self):
        PostFactory.create_a_post(client=self.client, text='This is the test post by the first user!',
                                  photo='unit_test_image')

        # create another user and create a post with that user.
        super().setUp(username='test_user2', email='test_user2@domain.com')
        super().authenticate()
        PostFactory.create_a_post(client=self.client, text='This is the first test post by the second user!',
                                  photo='unit_test_image2')
        PostFactory.create_a_post(client=self.client, text='This is the second test post by the second user!',
                                  photo='unit_test_image2')

        response = self.client.get(reverse('post-list'), data={'username': 'test_user2'})
        posts = response.json()['results']

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, response.json()['count'])

        self.assertEqual(self.user.id, posts[0]['user'])
        self.assertEqual('This is the second test post by the second user!', posts[0]['text'])
        self.assertIn('unit_test_image2', posts[0]['photo'])

        self.assertEqual(self.user.id, posts[1]['user'])
        self.assertEqual('This is the first test post by the second user!', posts[1]['text'])
        self.assertIn('unit_test_image', posts[1]['photo'])


class SortedFetchPostTest(FetchPostTest):
    """
    Test class for GET request to '/post-list' endpoint, with ordering.

    Command to run the tests of this class:
        make test module=posts.tests.test_posts_fetch.SortedFetchPostTest

    Note
    ____
    SortedFetchPostTest.test_fetch_posts_ordered_by_creation_date_latest_first is already covered by
    FetchPostTest.test_fetch_posts_multiple_posts_exist, as the default order criteria is '-created_at', i.e.,
    latest posts first, hence hasn't been implement here.

    """

    def test_fetch_posts_ordered_by_creation_date_oldest_first(self):
        PostFactory.create_a_post(client=self.client, text='This is the first test post!', photo='unit_test_image')
        PostFactory.create_a_post(client=self.client, text='This is the second test post!', photo='unit_test_image2')
        PostFactory.create_a_post(client=self.client, text='This is the third test post!', photo='unit_test_image')

        response = self.client.get(reverse('post-list'), data={
            'sort-by': 'created_at'
        })
        posts = response.json()['results']

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.json()['count'])

        self.assertEqual(self.user.id, posts[0]['user'])
        self.assertEqual('This is the first test post!', posts[0]['text'])
        self.assertIn('unit_test_image', posts[0]['photo'])

        self.assertEqual(self.user.id, posts[1]['user'])
        self.assertEqual('This is the second test post!', posts[1]['text'])
        self.assertIn('unit_test_image2', posts[1]['photo'])

        self.assertEqual(self.user.id, posts[2]['user'])
        self.assertEqual('This is the third test post!', posts[2]['text'])
        self.assertIn('unit_test_image', posts[2]['photo'])

    def test_fetch_posts_ordered_by_update_date_latest_first(self):
        PostFactory.create_a_post(client=self.client, text='This is the first test post!', photo='unit_test_image')
        PostFactory.create_a_post(client=self.client, text='This is the second test post!', photo='unit_test_image2')
        PostFactory.create_a_post(client=self.client, text='This is the third test post!', photo='unit_test_image')

        response = self.client.get(reverse('post-list'))
        post_id_of_the_post_to_be_updated = response.json()['results'][1]['id']

        PostFactory.update_a_post(client=self.client, post_id=post_id_of_the_post_to_be_updated,
                                  text='This is the updated second test post!')

        for sort_by in ['-updated_at', 'latest_first']:
            response = self.client.get(reverse('post-list'), data={
                'sort-by': sort_by
            })
            posts = response.json()['results']

            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(3, response.json()['count'])

            self.assertEqual(self.user.id, posts[0]['user'])
            self.assertEqual('This is the updated second test post!', posts[0]['text'])
            self.assertIn('unit_test_image2', posts[0]['photo'])

            self.assertEqual(self.user.id, posts[1]['user'])
            self.assertEqual('This is the third test post!', posts[1]['text'])
            self.assertIn('unit_test_image', posts[1]['photo'])

            self.assertEqual(self.user.id, posts[2]['user'])
            self.assertEqual('This is the first test post!', posts[2]['text'])
            self.assertIn('unit_test_image', posts[2]['photo'])

    def test_fetch_posts_ordered_by_update_date_oldest_first(self):
        PostFactory.create_a_post(client=self.client, text='This is the first test post!', photo='unit_test_image')
        PostFactory.create_a_post(client=self.client, text='This is the second test post!', photo='unit_test_image2')
        PostFactory.create_a_post(client=self.client, text='This is the third test post!', photo='unit_test_image')

        response = self.client.get(reverse('post-list'))
        post_id_of_the_post_to_be_updated = response.json()['results'][1]['id']

        PostFactory.update_a_post(client=self.client, post_id=post_id_of_the_post_to_be_updated,
                                  text='This is the updated second test post!')

        for sort_by in ['updated_at', 'oldest_first']:
            response = self.client.get(reverse('post-list'), data={
                'sort-by': sort_by
            })
            posts = response.json()['results']

            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(3, response.json()['count'])

            self.assertEqual(self.user.id, posts[0]['user'])
            self.assertEqual('This is the first test post!', posts[0]['text'])
            self.assertIn('unit_test_image', posts[0]['photo'])

            self.assertEqual(self.user.id, posts[1]['user'])
            self.assertEqual('This is the third test post!', posts[1]['text'])
            self.assertIn('unit_test_image', posts[1]['photo'])

            self.assertEqual(self.user.id, posts[2]['user'])
            self.assertEqual('This is the updated second test post!', posts[2]['text'])
            self.assertIn('unit_test_image2', posts[2]['photo'])

    def test_fetch_posts_ordered_by_username_ascending(self):
        first_user_id = self.user.id

        super().create_two_posts_from_two_different_users_and_switch_user()

        for sort_by in ['user__username', 'username_ascending']:
            response = self.client.get(reverse('post-list'), data={
                'sort-by': sort_by
            })
            posts = response.json()['results']

            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(2, response.json()['count'])

            self.assertEqual(first_user_id, posts[0]['user'])
            self.assertEqual('This is the test post by the first user!', posts[0]['text'])
            self.assertIn('unit_test_image', posts[0]['photo'])

            self.assertEqual(self.user.id, posts[1]['user'])
            self.assertEqual('This is the test post by the second user!', posts[1]['text'])
            self.assertIn('unit_test_image2', posts[1]['photo'])

    def test_fetch_posts_ordered_by_username_descending(self):
        first_user_id = self.user.id

        super().create_two_posts_from_two_different_users_and_switch_user()

        for sort_by in ['-user__username', 'username_descending']:
            response = self.client.get(reverse('post-list'), data={
                'sort-by': sort_by
            })
            posts = response.json()['results']

            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(2, response.json()['count'])

            self.assertEqual(self.user.id, posts[0]['user'])
            self.assertEqual('This is the test post by the second user!', posts[0]['text'])
            self.assertIn('unit_test_image2', posts[0]['photo'])

            self.assertEqual(first_user_id, posts[1]['user'])
            self.assertEqual('This is the test post by the first user!', posts[1]['text'])
            self.assertIn('unit_test_image', posts[1]['photo'])


class PaginatedFetchPostTest(FetchPostTest):
    """
        Test class for GET request to '/post-list' endpoint, to test pagination.

        Command to run the tests of this class:
            make test module=posts.tests.test_posts_fetch.PaginatedFetchPostTest

        Note
        ____
        """

    def generate_posts(self, num_posts):
        for i in range(num_posts):
            PostFactory.create_a_post(client=self.client, text=f'Post #{i}', photo='unit_test_image')

    def test_fetch_fifteen_posts_with_default_page_size(self):
        """
        The default pagination page size is 10 and the default ordering is by latest posts first.
        So, we should get the latest 10 posts, alongwith a url to fetch the second page.
        """
        self.generate_posts(15)

        response = self.client.get(reverse('post-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(10, len(response.json()['results']))
        self.assertIsNone(response.json()['previous'])

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(5, len(response.json()['results']))
        self.assertIsNone(response.json()['next'])

    def test_fetch_twenty_five_posts_with_default_page_size(self):
        """
        The default pagination page size is 10 and the default ordering is by latest posts first.
        So, we should get the latest 10 posts, alongwith a url to fetch the second page.
        """
        self.generate_posts(25)

        response = self.client.get(reverse('post-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(25, response.json()['count'])
        self.assertEqual(10, len(response.json()['results']))
        self.assertIsNone(response.json()['previous'])

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(25, response.json()['count'])
        self.assertEqual(10, len(response.json()['results']))

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(25, response.json()['count'])
        self.assertEqual(5, len(response.json()['results']))
        self.assertIsNone(response.json()['next'])

    def test_fetch_fifteen_posts_with_custom_page_size(self):
        self.generate_posts(15)

        response = self.client.get(reverse('post-list'), data={
            'page_size': 5
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(5, len(response.json()['results']))
        self.assertIsNone(response.json()['previous'])

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(5, len(response.json()['results']))

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(5, len(response.json()['results']))
        self.assertIsNone(response.json()['next'])

    def test_fetch_posts_with_greater_than_max_page_size(self):
        """
        The maximum page_size is 100, so if we define the page_size to be greater than that, only as many as page_size
        posts will be sent per page.
        """

        self.generate_posts(150)

        response = self.client.get(reverse('post-list'), data={
            'page_size': 150
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(150, response.json()['count'])
        self.assertEqual(100, len(response.json()['results']))
        self.assertIsNone(response.json()['previous'])

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(150, response.json()['count'])
        self.assertEqual(50, len(response.json()['results']))
        self.assertIsNone(response.json()['next'])

    def test_fetch_posts_with_zero_page_size(self):
        """
        If the page_size is set to 0, then the default page_size will be considered.
        """

        self.generate_posts(15)

        response = self.client.get(reverse('post-list'), data={
            'page_size': 0
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(10, len(response.json()['results']))
        self.assertIsNone(response.json()['previous'])

        url_to_fetch_next_page = response.json()['next']

        response = self.client.get(url_to_fetch_next_page)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(15, response.json()['count'])
        self.assertEqual(5, len(response.json()['results']))
        self.assertIsNone(response.json()['next'])

from tests.utils.registered_users_tests_base import RegisteredUsersTestBase
from posts.tests.utils.PostFactory import PostFactory

from posts.models import Post


class PostModelTest(RegisteredUsersTestBase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        super().authenticate()

    def test_fetch_a_post(self):
        post = PostFactory.create_a_post(client=self.client, text='This is a test post!', photo=None)
        post_id, post_username = post.json()['id'], post.json()['username']

        self.assertEqual(str(Post.objects.get(pk=post_id)),  # type: ignore
                         f"{post_username} - {'This is a test post!'[:10]}")

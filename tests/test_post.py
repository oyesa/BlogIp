import unittest
from app.models import Post


class TestPost(unittest.TestCase):
    def setUp(self):
        """Method that will run before every test"""
        self.new_post = Post(
            user_id=1,
            category_id=1,
            title="Test Title",
            content="Test Content",
            image_path="",
            created_at="2019-09-09"
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Post))

    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all()) > 0)

    def test_get_post_by_id(self):
        self.new_post.save_post()
        got_post = Post.get_post(1)
        self.assertTrue(got_post is not None)
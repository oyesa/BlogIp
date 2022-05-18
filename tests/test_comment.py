import unittest
from app.models import Comment


class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comment(
            content="A good time to be alive")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))
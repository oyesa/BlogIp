import unittest
from app.models import User


class TestUser(unittest.TestCase):
    def setUp(self):
        """Method that will run before every test"""
        self.new_user = User(
            username='Poh',
            name='Winnie Poh',
            email='winpoh@mail.com',
            password='winpoh7'
        )

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password
import unittest
import sys

from auth_plugin.config import config
from auth_plugin.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # Initialize the DatabaseManager with SQLite for testing
        self.db_manager = DatabaseManager(db_type=config.DB_TYPE, db_url=config.DB_URL)

    def test_add_user(self):
        self.db_manager.add_user(username="janedoe", email="janedoe@example.com")
        user = self.db_manager.get_user(user_id=1)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "janedoe")
        self.assertEqual(user.email, "janedoe@example.com")

    def test_get_user_nonexistent(self):
        user = self.db_manager.get_user(user_id=999)
        self.assertIsNone(user)

    def test_delete_user(self):
        self.db_manager.add_user(username="testuser", email="testuser@example.com")
        user = self.db_manager.get_user(user_id=1)
        self.db_manager.delete_user(user.id)
        user = self.db_manager.get_user(user_id=1)
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import pymongo
import sqlalchemy
from auth_plugin.db_manager import create_db_manager
from auth_plugin.db_manager.exceptions import (
    DBConnectionError,
    DBAuthenticationError,
    DBConfigurationError
)


class TestDBManager(unittest.TestCase):
    """Test cases for database manager factory and base functionality"""

    def test_invalid_db_type(self):
        with self.assertRaises(DBConfigurationError):
            create_db_manager(db_type="invalid", db_name="test")

    def test_missing_required_params(self):
        with self.assertRaises(DBConfigurationError):
            create_db_manager(db_type="mysql", db_name="")


class TestMongoDBManager(unittest.TestCase):
    """Test cases for MongoDB manager"""

    @patch('pymongo.MongoClient')
    def test_mongodb_connection_success(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db

        with create_db_manager(
            db_type="mongodb",
            db_name="test_db",
            host="localhost",
            port=27017
        ) as db:
            self.assertIsNotNone(db.client)
            self.assertIsNotNone(db.db)
            mock_client.assert_called_once()

    @patch('pymongo.MongoClient')
    def test_mongodb_auth_failure(self, mock_client):
        mock_client.side_effect = pymongo.errors.OperationFailure(
            "Authentication failed"
        )

        with self.assertRaises(DBAuthenticationError):
            create_db_manager(
                db_type="mongodb",
                db_name="test_db",
                user="wrong",
                password="wrong"
            )

    @patch('pymongo.MongoClient')
    def test_mongodb_connection_timeout(self, mock_client):
        mock_client.side_effect = pymongo.errors.ServerSelectionTimeoutError(
            "Connection timed out"
        )

        with self.assertRaises(DBConnectionError):
            create_db_manager(
                db_type="mongodb",
                db_name="test_db"
            )


class TestPostgresDBManager(unittest.TestCase):
    """Test cases for PostgreSQL manager"""

    @patch('sqlalchemy.create_engine')
    def test_postgres_connection_success(self, mock_engine):
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value = mock_connection

        with create_db_manager(
            db_type="postgresql",
            db_name="test_db",
            user="user",
            password="pass"
        ) as db:
            self.assertIsNotNone(db.client)
            self.assertIsNotNone(db.db)
            mock_engine.assert_called_once()

    @patch('sqlalchemy.create_engine')
    def test_postgres_connection_failure(self, mock_engine):
        mock_engine.side_effect = sqlalchemy.exc.OperationalError(
            "statement", "params", "orig"
        )

        with self.assertRaises(DBConnectionError):
            create_db_manager(
                db_type="postgresql",
                db_name="test_db",
                user="user",
                password="pass"
            )


class TestMySQLManager(unittest.TestCase):
    """Test cases for MySQL manager"""

    @patch('sqlalchemy.create_engine')
    def test_mysql_connection_success(self, mock_engine):
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value = mock_connection

        with create_db_manager(
            db_type="mysql",
            db_name="test_db",
            user="user",
            password="pass"
        ) as db:
            self.assertIsNotNone(db.client)
            self.assertIsNotNone(db.db)
            mock_engine.assert_called_once()

    @patch('sqlalchemy.create_engine')
    def test_mysql_auth_failure(self, mock_engine):
        mock_engine.side_effect = sqlalchemy.exc.OperationalError(
            "statement", "params", "Access denied"
        )

        with self.assertRaises(DBConnectionError):
            create_db_manager(
                db_type="mysql",
                db_name="test_db",
                user="wrong",
                password="wrong"
            )

    def test_mysql_missing_credentials(self):
        with self.assertRaises(DBConfigurationError):
            create_db_manager(
                db_type="mysql",
                db_name="test_db"
            )

    @patch('sqlalchemy.create_engine')
    def test_connection_ping(self, mock_engine):
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value = mock_connection

        with create_db_manager(
            db_type="mysql",
            db_name="test_db",
            user="user",
            password="pass"
        ) as db:
            self.assertTrue(db.ping())
            mock_connection.execute.assert_called_with("SELECT 1")


if __name__ == '__main__':
    unittest.main()

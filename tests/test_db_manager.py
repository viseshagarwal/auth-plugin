import unittest
from unittest.mock import patch, MagicMock
from auth_plugin.db_manager import DBManager  # Replace with the actual module name


class TestDBManagerQueries(unittest.TestCase):

    @patch("psycopg2.connect")
    def test_postgres_execute_query(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        db_manager = DBManager(
            db_type="postgres", db_name="test_db", user="user", password="password"
        )

        db_manager.execute_query("SELECT * FROM table_name")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM table_name", None)

    @patch("mysql.connector.connect")
    def test_mysql_execute_query(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        db_manager = DBManager(
            db_type="mysql", db_name="test_db", user="user", password="password"
        )

        db_manager.execute_query("SELECT * FROM table_name")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM table_name", None)

    @patch("psycopg2.connect")
    def test_postgres_fetch_results(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("row1",), ("row2",)]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        db_manager = DBManager(
            db_type="postgres", db_name="test_db", user="user", password="password"
        )

        results = db_manager.fetch_results()
        self.assertEqual(results, [("row1",), ("row2",)])
        mock_cursor.fetchall.assert_called_once()

    @patch("mysql.connector.connect")
    def test_mysql_fetch_results(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"column1": "value1"},
            {"column2": "value2"},
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        db_manager = DBManager(
            db_type="mysql", db_name="test_db", user="user", password="password"
        )

        results = db_manager.fetch_results()
        self.assertEqual(results, [{"column1": "value1"}, {"column2": "value2"}])
        mock_cursor.fetchall.assert_called_once()


if __name__ == "__main__":
    unittest.main()

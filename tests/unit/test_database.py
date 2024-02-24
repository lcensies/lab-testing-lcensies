import unittest
from unittest.mock import MagicMock, patch
from app.database import Database


def normalize_sql(sql):
    """Remove newlines and leading/trailing whitespace from SQL commands."""
    return " ".join(sql.split())


# TODO: refactor mocking cursor and conn setup


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = ":memory:"
        self.database = Database(self.db_path)

    @patch("app.database.sqlite3.connect")
    def test_add_customer(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db = Database()
        db.add_customer("John Doe", "123 Main St")

        expected_sql = normalize_sql(
            "INSERT INTO customers (name, address) VALUES (?, ?)"
        )
        actual_sql = normalize_sql(mock_cursor.execute.call_args[0][0])

        self.assertEqual(expected_sql, actual_sql)
        self.assertEqual(
            mock_cursor.execute.call_args[0][1], ("John Doe", "123 Main St")
        )

    @patch("app.database.sqlite3.connect")
    def test_get_customer(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, "John Doe", "123 Main St")
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db = Database()
        result = db.get_customer(1)

        expected_sql = normalize_sql("SELECT * FROM customers WHERE customer_id = ?")
        actual_sql = normalize_sql(mock_cursor.execute.call_args[0][0])

        self.assertEqual(expected_sql, actual_sql)
        self.assertEqual(mock_cursor.execute.call_args[0][1], (1,))
        self.assertEqual(result, (1, "John Doe", "123 Main St"))

    @patch("app.database.sqlite3.connect")
    def test_update_customer(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db = Database()
        db.update_customer(1, "Jane Doe", "456 Maple Avenue")

        # Retrieve the actual SQL command used in the `execute` call
        called_sql = mock_cursor.execute.call_args[0][0]
        # Normalize both the expected and actual SQL commands before comparing
        expected_sql = normalize_sql(
            "UPDATE customers SET name = ?, address = ? WHERE customer_id = ?"
        )
        actual_sql = normalize_sql(called_sql)

        self.assertEqual(expected_sql, actual_sql)
        # Also, assert the parameters are passed correctly
        self.assertEqual(
            mock_cursor.execute.call_args[0][1], ("Jane Doe", "456 Maple Avenue", 1)
        )

    @patch("app.database.sqlite3.connect")
    def test_delete_customer(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db = Database()
        db.delete_customer(1)

        expected_sql = normalize_sql("DELETE FROM customers WHERE customer_id = ?")
        actual_sql = normalize_sql(mock_cursor.execute.call_args[0][0])

        self.assertEqual(expected_sql, actual_sql)
        self.assertEqual(mock_cursor.execute.call_args[0][1], (1,))

    @patch("app.database.sqlite3.connect")
    def test_get_all_customers(self, mock_connect):
        # Setup expected data
        expected_customers = [
            (1, "John Doe", "123 Elm Street"),
            (2, "Jane Doe", "456 Maple Avenue"),
        ]

        # Mocking the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = expected_customers

        # Initialize Database object and call get_all_customers
        db = Database()
        customers = db.get_all_customers()

        # Assertions to validate the behavior
        self.assertEqual(customers, expected_customers)
        mock_cursor.execute.assert_called_with(
            "SELECT * FROM customers ORDER BY customer_id ASC"
        )


if __name__ == "__main__":
    unittest.main()

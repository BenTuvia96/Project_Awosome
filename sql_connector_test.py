import unittest
from sql_connector import SQLConnector

class TestFinanceManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the database connection and class-wide variables."""
        cls.manager = SQLConnector(host="localhost", database="project_awsome", user="root", password="Aa123456")
        cls.user_id = None
        cls.transaction_id = None

    @classmethod
    def tearDownClass(cls):
        """Close the database connection at the end of tests."""
        cls.manager.close_connection()

    def test_insert_user(self):
        self.manager.insert_user("TestUser", "hashed_password", "testuser@email.com", "Test User")
        # Assuming there's an auto-increment ID, the user_id should be greater than 0
        self.assertTrue(self.manager.get_user_balance(1) is not None)
        self.__class__.user_id = 1

    def test_insert_transaction(self):
        self.manager.insert_transaction(self.user_id, "2023-08-17", "Test Lunch", "Food", 10.50, "EXPENSE")
        # Check the balance after the transaction
        balance = self.manager.get_user_balance(self.user_id)
        self.assertEqual(balance, -10.50)
        self.__class__.transaction_id = 1

    def test_update_user_info(self):
        self.manager.update_user_info(self.user_id, username="UpdatedTestUser")
        # Add logic to fetch the updated user and check if the username is indeed "UpdatedTestUser"

    def test_update_transaction(self):
        self.manager.update_transaction(self.transaction_id, description="Updated Test Lunch")
        # Add logic to fetch the updated transaction and check if the description is indeed "Updated Test Lunch"

    def test_get_transactions_for_user(self):
        transactions = self.manager.get_transactions_for_user(self.user_id)
        self.assertTrue(len(transactions) > 0)  # Assuming the transaction was inserted successfully

    def test_delete_transaction(self):
        self.manager.delete_transaction(self.transaction_id)
        # Add logic to try fetching the deleted transaction and ensure it's not found

    def test_get_user_transactions_in_date_range(self):
        transactions = self.manager.get_user_transactions_in_date_range(self.user_id, "2023-08-01", "2023-08-31")
        self.assertTrue(len(transactions) == 0)  # Since we deleted the transaction

if __name__ == "__main__":
    unittest.main()

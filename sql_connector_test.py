from sql_connector import SQLConnector


def test_finance_manager_operations():
    # Initialize the FinanceManager instance
    manager = SQLConnector(host="localhost", database="project_awsome", user="root", password="Aa123456")

    # Insert a new user
    manager.insert_user("TestUser", "test_password", "test@email.com", "Test User")
    user_id = manager.get_user_id_by_username("TestUser")
    assert user_id is not None

    # Insert a balance for the user
    initial_balance = 1000.00
    manager.insert_balance(user_id, initial_balance)
    balance = manager.get_user_balance(user_id)
    assert balance == initial_balance

    # Insert a transaction (e.g., an EXPENSE of 100.00)
    manager.insert_transaction(user_id, "2023-08-16", "Test Transaction", "Test", 100.00, "EXPENSE")
    balance_after_transaction = manager.get_user_balance(user_id)
    assert balance_after_transaction == initial_balance - 100.00

    # Update the transaction to INCOME of 200.00
    transaction_id = manager.get_last_transaction_id_for_user(
        user_id)  # Assuming you have a method to get the last transaction ID for a user
    manager.update_transaction(transaction_id, amount=200.00, transaction_type="INCOME")
    balance_after_update = manager.get_user_balance(user_id)
    assert balance_after_update == balance_after_transaction + 200.00 + 100.00  # Reversed the expense and added the income

    # Delete the transaction and check if balance is adjusted correctly
    manager.delete_transaction(transaction_id)
    balance_after_deletion = manager.get_user_balance(user_id)
    assert balance_after_deletion == initial_balance

    print("All tests passed!")


test_finance_manager_operations()

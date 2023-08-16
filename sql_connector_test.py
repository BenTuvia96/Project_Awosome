from sql_connector import SQLConnector


def test_finance_manager_operations():
    # Initialize the FinanceManager instance
    manager = SQLConnector(host="localhost", database="project_awsome", user="root", password="Aa123456")

    # Insert a new user
    manager.insert_user("TestUser", "test_password", "test@email.com", "Test User")
    user_id = manager.get_user_id_by_username("TestUser")
    assert user_id is not None

    print(manager.get_user_info(1))

    print("All tests passed!")


test_finance_manager_operations()

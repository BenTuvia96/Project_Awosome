import mysql.connector
from mysql.connector import Error


class SQLConnector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = self.create_connection()

    def create_connection(self):
        """Create a database connection and return the connection object."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                print("Successfully connected to the database.")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def insert_user(self, username, password, email, full_name):
        """Insert a new user into the users table."""
        query = """INSERT INTO users (username, password, email, full_name) 
                   VALUES (%s, %s, %s, %s)"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (username, password, email, full_name))
            self.connection.commit()
            print(f"User {username} added successfully.")
        except Error as e:
            print(f"Error: {e}")

    def get_user_balance(self, user_id):
        """Retrieve the current balance for a given user."""
        query = """SELECT current_balance FROM balances WHERE user_id = %s"""
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_user_balance(self, user_id, amount):
        """Update the balance for a given user."""
        current_balance = self.get_user_balance(user_id)
        if current_balance is not None:
            new_balance = float(current_balance) + float(amount)
            query = """UPDATE balances SET current_balance = %s, time_updated = NOW() WHERE user_id = %s"""
            cursor = self.connection.cursor()
            cursor.execute(query, (new_balance, user_id))
            self.connection.commit()
        else:
            # If the user doesn't have a balance entry, insert a new one
            self.insert_balance(user_id, amount)

    def insert_transaction(self, user_id, date, description, category, amount, transaction_type):
        """Insert a new transaction into the transactions table and update the user's balance."""
        query = """INSERT INTO transactions (user_id, date, description, category, amount, transaction_type) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (user_id, date, description, category, amount, transaction_type))
            self.connection.commit()

            # Update the balance based on the transaction type
            if transaction_type == 'EXPENSE':
                self.update_user_balance(user_id, -amount)
            elif transaction_type == 'INCOME':
                self.update_user_balance(user_id, amount)

            print("Transaction added successfully.")
        except Error as e:
            print(f"Error: {e}")

    def insert_balance(self, user_id, current_balance):
        """Insert a new balance into the balances table."""
        query = """INSERT INTO balances (user_id, current_balance) 
                   VALUES (%s, %s)"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (user_id, current_balance))
            self.connection.commit()
            print("Balance added successfully.")
        except Error as e:
            print(f"Error: {e}")

    def update_user_info(self, user_id, username=None, password=None, email=None, full_name=None):
        """Update user information."""
        updates = []
        values = []

        if username:
            updates.append("username = %s")
            values.append(username)

        if password:
            updates.append("password = %s")
            values.append(password)

        if email:
            updates.append("email = %s")
            values.append(email)

        if full_name:
            updates.append("full_name = %s")
            values.append(full_name)

        values.append(user_id)

        query = "UPDATE users SET " + ", ".join(updates) + " WHERE user_id = %s"

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(values))
            self.connection.commit()
            print(f"User {user_id} updated successfully.")
        except Error as e:
            print(f"Error: {e}")


    def get_transaction(self, transaction_id):
        """Retrieve the details of a specific transaction."""
        query = "SELECT * FROM transactions WHERE transaction_id = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (transaction_id,))
        return cursor.fetchone()

    def update_transaction(self, transaction_id, date=None, description=None, category=None, amount=None,
                           transaction_type=None):
        """Update transaction information and adjust the user's balance accordingly."""
        # Get the old transaction details
        old_transaction = self.get_transaction(transaction_id)

        if not old_transaction:
            print(f"Transaction with ID {transaction_id} not found.")
            return

        old_amount = old_transaction[5]
        old_type = old_transaction[6]

        # If the transaction type or amount hasn't been provided for update, use the old values
        if not transaction_type:
            transaction_type = old_type

        if not amount:
            amount = old_amount

        # Adjust balance based on old transaction details
        if old_type == 'EXPENSE':
            self.update_user_balance(old_transaction[1], old_amount)
        elif old_type == 'INCOME':
            self.update_user_balance(old_transaction[1], -old_amount)

        # Update the transaction in the database
        updates = []
        values = []

        if date:
            updates.append("date = %s")
            values.append(date)

        if description:
            updates.append("description = %s")
            values.append(description)

        if category:
            updates.append("category = %s")
            values.append(category)

        if amount:
            updates.append("amount = %s")
            values.append(amount)

        if transaction_type:
            updates.append("transaction_type = %s")
            values.append(transaction_type)

        values.append(transaction_id)

        query = "UPDATE transactions SET " + ", ".join(updates) + " WHERE transaction_id = %s"

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(values))
            self.connection.commit()

            # Adjust balance based on the updated transaction details
            if transaction_type == 'EXPENSE':
                self.update_user_balance(old_transaction[1], -amount)
            elif transaction_type == 'INCOME':
                self.update_user_balance(old_transaction[1], amount)

            print(f"Transaction {transaction_id} updated successfully.")
        except Error as e:
            print(f"Error: {e}")

    def get_transactions_for_user(self, user_id):
        """Retrieve all transactions for a specific user."""
        query = "SELECT * FROM transactions WHERE user_id = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    def delete_transaction(self, transaction_id):
        """Delete a transaction by its ID and adjust the user's balance accordingly."""

        # Get the old transaction details
        old_transaction = self.get_transaction(transaction_id)

        if not old_transaction:
            print(f"Transaction with ID {transaction_id} not found.")
            return

        old_amount = old_transaction[5]
        old_type = old_transaction[6]

        # Adjust balance based on old transaction details
        if old_type == 'EXPENSE':
            self.update_user_balance(old_transaction[1], old_amount)
        elif old_type == 'INCOME':
            self.update_user_balance(old_transaction[1], -old_amount)

        # Delete the transaction from the database
        query = "DELETE FROM transactions WHERE transaction_id = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (transaction_id,))
            self.connection.commit()
            print(f"Transaction {transaction_id} deleted successfully.")
        except Error as e:
            print(f"Error: {e}")

    def get_user_transactions_in_date_range(self, user_id, start_date, end_date):
        """Retrieve a user's transactions within a specific date range."""
        query = """SELECT * FROM transactions WHERE user_id = %s AND date BETWEEN %s AND %s"""
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id, start_date, end_date))
        return cursor.fetchall()

    def get_user_id_by_username(self, username):
        """Retrieve a user's ID by their username."""
        query = """SELECT user_id FROM users WHERE username = %s"""
        cursor = self.connection.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_last_transaction_id_for_user(self, user_id):
        """Retrieve the ID of the last transaction for a given user."""
        query = """SELECT transaction_id FROM transactions WHERE user_id = %s ORDER BY transaction_id DESC LIMIT 1"""
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


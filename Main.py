import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = self.connect(host, user, password, database)

    def connect(self, host, user, password, database):
        """Establish connection to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if connection.is_connected():
                print("Successfully connected to the database")
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def close(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def execute_query(self, query, params=None):
        """Execute a single query."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Fetch all results of a query."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        cursor.close()
        return records

# Usage:
if __name__ == "__main__":
    # These should ideally come from a config file or environment variables.
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'your_password'
    DATABASE = 'your_database'

    db_manager = DatabaseManager(HOST, USER, PASSWORD, DATABASE)

    # Test fetching some data
    records = db_manager.fetch_all("SELECT * FROM some_table")
    for row in records:
        print(row)

    db_manager.close()

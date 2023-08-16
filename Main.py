import mysql.connector

# Database Configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aa123456',
    'database': 'trial1'
}

# Connect to MySQL database
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# SQL Statement to create the table if it doesn't exist
create_table_sql = """
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    description VARCHAR(255),
    category VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('INCOME', 'EXPENSE') NOT NULL
)
"""

cursor.execute(create_table_sql)

# Data to be inserted
transaction_data = {
    'date': '2023-08-15',
    'description': 'Bought Groceries',
    'category': 'Food',
    'amount': 50.25,
    'transaction_type': 'EXPENSE'
}

# SQL Insert Statement
insert_sql = ("INSERT INTO transactions (date, description, category, amount, transaction_type) "
              "VALUES (%(date)s, %(description)s, %(category)s, %(amount)s, %(transaction_type)s)")

cursor.execute(insert_sql, transaction_data)

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("Transaction data inserted successfully!")

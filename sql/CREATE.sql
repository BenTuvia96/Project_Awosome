-- Creating the `users` table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- This length assumes a bcrypt hash or similar. Adjust if necessary.
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    time_joined TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATE
);

-- Creating the `transactions` table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE NOT NULL,
    description VARCHAR(255),
    category VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('INCOME', 'EXPENSE') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE -- Ensuring relationship with `users` table
);

-- Creating the `balances` table
CREATE TABLE balances (
    balance_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    current_balance DECIMAL(10, 2) NOT NULL,
    time_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE -- Ensuring relationship with `users` table
);

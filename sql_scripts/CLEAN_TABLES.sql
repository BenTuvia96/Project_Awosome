-- Delete all data from the tables
DELETE FROM transactions;
DELETE FROM balances;
DELETE FROM users;

-- Reset auto-increment values
ALTER TABLE transactions AUTO_INCREMENT = 1;
ALTER TABLE balances AUTO_INCREMENT = 1;
ALTER TABLE users AUTO_INCREMENT = 1;

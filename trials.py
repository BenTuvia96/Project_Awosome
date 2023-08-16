import bcrypt

def hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(stored_password: bytes, provided_password: str) -> bool:
    """Check if a provided password matches the stored hashed version."""
    try:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
    except ValueError:
        return False


# Assume this is a new user registering
user_id = "user123"
user_plain_password = "SecurePass123"

# This will simulate our "database" (in this case, just a dictionary)
user_db = {}

# Hash the user's password and "store" it
user_db[user_id] = hash_password(user_plain_password)

# Now, let's simulate a login attempt
login_user_id = "user123"
login_attempt_password = "SecurePass123"  # Correct password in this case

# Check if the user exists and if the password is correct
if login_user_id in user_db:
    stored_password = user_db[login_user_id]
    if verify_password(stored_password, login_attempt_password):
        print(f"Welcome back, {login_user_id}!")
    else:
        print("Incorrect password!")
else:
    print("User does not exist!")

import sqlite3
import re
import hashlib
import os

# Function to validate if the input username is safe and properly formatted
def validate_username(username):
    if len(username) < 5 or len(username) > 20:
        raise ValueError("Username must be between 5 and 20 characters.")
    
    # Ensure that the username only contains letters, numbers, underscores, or hyphens
    if not re.match("^[a-zA-Z0-9_-]*$", username):
        raise ValueError("Username can only contain alphanumeric characters, underscores, or hyphens.")
    
    return username

# Function to hash passwords securely using PBKDF2 (sha256)
def hash_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    
    # Salted password hash for added security
    salt = os.urandom(16)  # Generate random salt
    hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    return salt + hashed_pw  # Return salted and hashed password

# Function to insert a new user to the database (for testing the password)
def insert_user_to_db(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    try:
        # Validate the username
        validate_username(username)
        
        # Hash the password with a salt
        hashed_pw = hash_password(password)
        
        # Insert new user into the database (username, hashed password)
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(query, (username, hashed_pw))
        connection.commit()
    
    except Exception as e:
        print(f"An error occurred while inserting user: {e}")
    
    finally:
        connection.close()

# Function to check credentials safely using prepared statements
def authenticate_user(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    try:
        # Validate the username
        validate_username(username)
        
        # Use parameterized queries to avoid SQL injection risk
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        
        user_data = cursor.fetchone()
        if user_data:
            # Compare the hashed password with the stored one
            stored_salt = user_data[1][:16]  # Extract salt from stored hash
            stored_hash = user_data[1][16:]  # Extract hashed password from stored hash
            
            hashed_input_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt, 100000)
            
            if hashed_input_pw == stored_hash:
                return "Authentication successful!"
            else:
                return "Invalid credentials!"
        else:
            return "User not found!"
    
    except Exception as e:
        return f"An error occurred: {e}"
    
    finally:
        connection.close()

# Example of how to use these functions
def main():
    # First, insert a new user to test
    insert_user_to_db('john_doe', 'securepassword123')

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    result = authenticate_user(username, password)
    print(result)


if __name__ == "__main__":
    main()

import sqlite3
import hashlib
import os
from datetime import datetime

DATABASE_FILE = 'users.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            google_auth BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create sessions table (optional, for better session management)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create admin user if it doesn't exist
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        admin_password_hash = hash_password('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', ('admin', 'admin@example.com', admin_password_hash))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return hash_password(password) == password_hash

def create_user(username, email, password, google_auth=False):
    """Create a new user in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password) if password else None
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, google_auth)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, google_auth))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError as e:
        conn.close()
        if 'username' in str(e):
            return False, 'Username already exists'
        elif 'email' in str(e):
            return False, 'Email already exists'
        return False, 'User creation failed'

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_user(username, password):
    """Authenticate a user with username and password"""
    user = get_user_by_username(username)
    if user and user['password_hash']:
        if verify_password(password, user['password_hash']):
            update_last_login(user['id'])
            return True, dict(user)
    return False, None

def update_last_login(user_id):
    """Update the last login timestamp for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users 
        SET last_login = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    """Get all users from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, created_at, last_login FROM users')
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]

def delete_user(username):
    """Delete a user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

if __name__ == '__main__':
    # Initialize the database when run directly
    init_db()

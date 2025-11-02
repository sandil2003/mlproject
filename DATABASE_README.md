# Database Setup Guide

## Overview
This project uses SQLite database for user authentication and management. The database provides secure password hashing and supports both regular authentication and Google OAuth.

## Database Structure

### Users Table
The `users` table stores all user information:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| username | TEXT | Unique username |
| email | TEXT | Unique email address |
| password_hash | TEXT | SHA-256 hashed password (NULL for Google auth users) |
| google_auth | BOOLEAN | Flag indicating Google authentication |
| created_at | TIMESTAMP | Account creation timestamp |
| last_login | TIMESTAMP | Last successful login timestamp |

### User Sessions Table (Optional)
The `user_sessions` table can be used for advanced session management:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| user_id | INTEGER | Foreign key to users table |
| session_token | TEXT | Unique session identifier |
| created_at | TIMESTAMP | Session creation time |
| expires_at | TIMESTAMP | Session expiration time |

## Database File
- **File Name**: `users.db`
- **Location**: Project root directory
- **Created Automatically**: Yes, on first run

## Initialization

### Automatic Initialization
The database is automatically initialized when you run the application:
```bash
python app.py
```

### Manual Initialization
You can also initialize the database manually:
```bash
python database.py
```

## Default Admin Account
A default admin account is created during initialization:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

**Important**: Change the admin password in production!

## Security Features

### Password Hashing
- Passwords are hashed using SHA-256 algorithm
- Plain text passwords are never stored in the database
- Hash verification is done securely during authentication

### SQL Injection Prevention
- All queries use parameterized statements
- User input is properly sanitized

## Available Functions

### Database Module (`database.py`)

#### Connection
```python
get_db_connection()  # Returns SQLite connection object
```

#### Initialization
```python
init_db()  # Creates tables and default admin user
```

#### User Management
```python
# Create a new user
create_user(username, email, password, google_auth=False)
# Returns: (success: bool, result: user_id or error_message)

# Authenticate user
authenticate_user(username, password)
# Returns: (success: bool, user_dict or None)

# Get user by username
get_user_by_username(username)
# Returns: user object or None

# Get user by email
get_user_by_email(email)
# Returns: user object or None

# Get all users
get_all_users()
# Returns: list of user dictionaries

# Delete user
delete_user(username)
# Returns: True if deleted, False otherwise

# Update last login
update_last_login(user_id)
# Updates the last_login timestamp
```

#### Password Functions
```python
# Hash a password
hash_password(password)
# Returns: SHA-256 hash string

# Verify password
verify_password(password, password_hash)
# Returns: True if match, False otherwise
```

## Database Backup

To backup your database:
```bash
# Windows
copy users.db users_backup.db

# Linux/Mac
cp users.db users_backup.db
```

## Database Inspection

You can inspect the database using SQLite command-line tool:

```bash
sqlite3 users.db
```

Common queries:
```sql
-- List all users
SELECT * FROM users;

-- Count total users
SELECT COUNT(*) FROM users;

-- Find users by email domain
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Show recent logins
SELECT username, last_login FROM users ORDER BY last_login DESC LIMIT 10;
```

## Troubleshooting

### Database Locked Error
If you get a "database is locked" error:
1. Close all connections to the database
2. Make sure only one instance of the app is running
3. Restart the application

### Corrupted Database
If the database gets corrupted:
1. Stop the application
2. Delete `users.db` file
3. Restart the application (will recreate the database)
4. Note: All user data will be lost

### Migration from JSON
If you were using JSON storage before:
1. The old `users.json` file is no longer used
2. Users will need to re-register their accounts
3. Or you can write a migration script to import data

## Upgrading Password Security

For production use, consider upgrading to bcrypt or Argon2:

```python
# Install bcrypt
pip install bcrypt

# In database.py, replace SHA-256 with bcrypt:
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash.encode())
```

## Production Recommendations

1. **Backup Strategy**: Implement regular database backups
2. **Password Policy**: Enforce stronger password requirements
3. **Rate Limiting**: Add login attempt rate limiting
4. **Session Management**: Implement proper session expiration
5. **Database Migration**: Use tools like Alembic for schema changes
6. **Connection Pooling**: For high-traffic applications
7. **Monitoring**: Log database operations and errors

## File Structure
```
mlproject/
├── app.py                  # Main Flask application
├── database.py            # Database operations
├── users.db               # SQLite database file (auto-created)
└── DATABASE_README.md     # This file
```

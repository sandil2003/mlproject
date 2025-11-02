#!/usr/bin/env python
"""
Database Management Script
Use this script to view and manage users in the database
"""

from database import (
    get_all_users, 
    create_user, 
    delete_user, 
    get_user_by_username,
    authenticate_user
)
import sys

def display_all_users():
    """Display all users in the database"""
    users = get_all_users()
    if not users:
        print("No users found in the database.")
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created At':<20}")
    print("="*80)
    
    for user in users:
        print(f"{user['id']:<5} {user['username']:<20} {user['email']:<30} {str(user['created_at']):<20}")
    
    print("="*80)
    print(f"Total users: {len(users)}\n")

def add_user():
    """Add a new user to the database"""
    print("\n--- Add New User ---")
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    
    if not username or not email or not password:
        print("Error: All fields are required!")
        return
    
    success, result = create_user(username, email, password)
    
    if success:
        print(f"Success! User '{username}' created with ID: {result}")
    else:
        print(f"Error: {result}")

def remove_user():
    """Remove a user from the database"""
    print("\n--- Delete User ---")
    username = input("Enter username to delete: ").strip()
    
    if not username:
        print("Error: Username is required!")
        return
    
    # Check if user exists
    user = get_user_by_username(username)
    if not user:
        print(f"Error: User '{username}' not found!")
        return
    
    confirm = input(f"Are you sure you want to delete user '{username}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        if delete_user(username):
            print(f"Success! User '{username}' has been deleted.")
        else:
            print(f"Error: Failed to delete user '{username}'.")
    else:
        print("Deletion cancelled.")

def test_login():
    """Test user authentication"""
    print("\n--- Test Login ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    success, user = authenticate_user(username, password)
    
    if success:
        print(f"\n✓ Authentication successful!")
        print(f"User ID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
    else:
        print("\n✗ Authentication failed! Invalid username or password.")

def search_user():
    """Search for a user"""
    print("\n--- Search User ---")
    username = input("Enter username to search: ").strip()
    
    user = get_user_by_username(username)
    
    if user:
        print("\nUser found:")
        print(f"  ID: {user['id']}")
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Google Auth: {'Yes' if user['google_auth'] else 'No'}")
        print(f"  Created At: {user['created_at']}")
        print(f"  Last Login: {user['last_login'] or 'Never'}")
    else:
        print(f"User '{username}' not found!")

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("  Database Management Tool")
    print("="*50)
    print("1. View all users")
    print("2. Add new user")
    print("3. Delete user")
    print("4. Search user")
    print("5. Test login")
    print("6. Exit")
    print("="*50)

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'list':
            display_all_users()
        elif command == 'add':
            add_user()
        elif command == 'delete':
            remove_user()
        elif command == 'search':
            search_user()
        elif command == 'test':
            test_login()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python manage_db.py [list|add|delete|search|test]")
        return
    
    # Interactive mode
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            display_all_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            remove_user()
        elif choice == '4':
            search_user()
        elif choice == '5':
            test_login()
        elif choice == '6':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")

if __name__ == '__main__':
    main()

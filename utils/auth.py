import hashlib
import json
import os
from datetime import datetime

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    users_file = "data/users.json"
    
    if not os.path.exists(users_file):
        return None
    
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
    except:
        return None
    
    hashed_password = hash_password(password)
    
    for user in users:
        if user['email'] == email and user['password'] == hashed_password:
            return {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'type': user['type'],
                'location': user['location'],
                'created_at': user['created_at']
            }
    
    return None

def create_user(name, email, phone, password, user_type, location):
    """Create a new user account"""
    users_file = "data/users.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Load existing users or create empty list
    users = []
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                users = json.load(f)
        except:
            users = []
    
    # Check if email already exists
    for user in users:
        if user['email'] == email:
            return None  # Email already exists
    
    # Create new user
    new_user = {
        'id': len(users) + 1,
        'name': name,
        'email': email,
        'phone': phone,
        'password': hash_password(password),
        'type': user_type,
        'location': location,
        'created_at': datetime.now().isoformat(),
        'verified': False,
        'rating': 0,
        'total_transactions': 0
    }
    
    users.append(new_user)
    
    # Save to file
    try:
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        return {
            'id': new_user['id'],
            'name': new_user['name'],
            'email': new_user['email'],
            'phone': new_user['phone'],
            'type': new_user['type'],
            'location': new_user['location'],
            'created_at': new_user['created_at']
        }
    except:
        return None

def get_user_by_email(email):
    """Get user information by email"""
    users_file = "data/users.json"
    
    if not os.path.exists(users_file):
        return None
    
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
    except:
        return None
    
    for user in users:
        if user['email'] == email:
            return user
    
    return None

def update_user_profile(email, updates):
    """Update user profile information"""
    users_file = "data/users.json"
    
    if not os.path.exists(users_file):
        return False
    
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
    except:
        return False
    
    for i, user in enumerate(users):
        if user['email'] == email:
            for key, value in updates.items():
                if key in user and key != 'id' and key != 'email' and key != 'password':
                    users[i][key] = value
            
            # Save updated users
            try:
                with open(users_file, 'w') as f:
                    json.dump(users, f, indent=2)
                return True
            except:
                return False
    
    return False

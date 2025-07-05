import json
import os
from datetime import datetime, timedelta
import random

def get_user_products(user_email):
    """Get products belonging to a specific user"""
    products_file = "data/products.json"
    
    if not os.path.exists(products_file):
        return []
    
    try:
        with open(products_file, 'r') as f:
            products = json.load(f)
    except:
        return []
    
    user_products = [p for p in products if p.get('seller_email') == user_email]
    return user_products

def get_all_products():
    """Get all available products"""
    products_file = "data/products.json"
    
    if not os.path.exists(products_file):
        # Create sample products if file doesn't exist
        return create_sample_products()
    
    try:
        with open(products_file, 'r') as f:
            products = json.load(f)
        return products
    except:
        return create_sample_products()

def create_sample_products():
    """Create sample products for demonstration"""
    from data.crops import AFRICAN_CROPS
    
    products = []
    for i, crop in enumerate(AFRICAN_CROPS[:20]):  # First 20 crops
        product = {
            'id': i + 1,
            'name': crop['name'],
            'category': crop['category'],
            'price': crop['price_per_kg'],
            'quantity': random.randint(50, 500),
            'description': f"Fresh {crop['name']} from {crop['region']}",
            'seller_email': f"farmer{i+1}@example.com",
            'seller_name': f"Farmer {i+1}",
            'location': crop['region'],
            'image_url': f"https://via.placeholder.com/300x200?text={crop['name']}",
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews_count': random.randint(5, 50),
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            'harvest_date': (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat(),
            'expiry_date': (datetime.now() + timedelta(days=random.randint(7, 30))).isoformat(),
            'organic': random.choice([True, False]),
            'available': True
        }
        products.append(product)
    
    # Save to file
    os.makedirs("data", exist_ok=True)
    try:
        with open("data/products.json", 'w') as f:
            json.dump(products, f, indent=2)
    except:
        pass
    
    return products

def add_product(product_data):
    """Add a new product to the database"""
    products_file = "data/products.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Load existing products or create empty list
    products = []
    if os.path.exists(products_file):
        try:
            with open(products_file, 'r') as f:
                products = json.load(f)
        except:
            products = []
    
    # Add new product
    new_product = {
        'id': len(products) + 1,
        'created_at': datetime.now().isoformat(),
        'available': True,
        'rating': 0,
        'reviews_count': 0,
        **product_data
    }
    
    products.append(new_product)
    
    # Save to file
    try:
        with open(products_file, 'w') as f:
            json.dump(products, f, indent=2)
        return new_product
    except:
        return None

def get_user_messages(user_email):
    """Get messages for a specific user"""
    messages_file = "data/messages.json"
    
    if not os.path.exists(messages_file):
        return create_sample_messages(user_email)
    
    try:
        with open(messages_file, 'r') as f:
            messages = json.load(f)
    except:
        return create_sample_messages(user_email)
    
    user_messages = [m for m in messages if m.get('to') == user_email or m.get('from') == user_email]
    return user_messages

def create_sample_messages(user_email):
    """Create sample messages for demonstration"""
    messages = [
        {
            'id': 1,
            'from': 'farmer1@example.com',
            'to': user_email,
            'subject': 'Maize Quality Inquiry',
            'content': 'Hello! I\'m interested in your maize. Can you tell me more about the quality and harvest date?',
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'read': False
        },
        {
            'id': 2,
            'from': 'buyer2@example.com',
            'to': user_email,
            'subject': 'Bulk Order Request',
            'content': 'Hi, I would like to place a bulk order for 500kg of rice. What\'s your best price?',
            'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
            'read': True
        },
        {
            'id': 3,
            'from': 'system@samaagrolink.com',
            'to': user_email,
            'subject': 'Market Price Alert',
            'content': 'The price of cassava in your region has increased by 15% this week. This might be a good time to sell!',
            'timestamp': (datetime.now() - timedelta(days=3)).isoformat(),
            'read': False
        }
    ]
    
    # Save to file
    os.makedirs("data", exist_ok=True)
    try:
        with open("data/messages.json", 'w') as f:
            json.dump(messages, f, indent=2)
    except:
        pass
    
    return messages

def add_message(from_email, to_email, subject, content):
    """Add a new message to the database"""
    messages_file = "data/messages.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Load existing messages or create empty list
    messages = []
    if os.path.exists(messages_file):
        try:
            with open(messages_file, 'r') as f:
                messages = json.load(f)
        except:
            messages = []
    
    # Add new message
    new_message = {
        'id': len(messages) + 1,
        'from': from_email,
        'to': to_email,
        'subject': subject,
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'read': False
    }
    
    messages.append(new_message)
    
    # Save to file
    try:
        with open(messages_file, 'w') as f:
            json.dump(messages, f, indent=2)
        return new_message
    except:
        return None

def get_transactions(user_email=None):
    """Get transaction history"""
    transactions_file = "data/transactions.json"
    
    if not os.path.exists(transactions_file):
        return create_sample_transactions(user_email)
    
    try:
        with open(transactions_file, 'r') as f:
            transactions = json.load(f)
    except:
        return create_sample_transactions(user_email)
    
    if user_email:
        user_transactions = [t for t in transactions if t.get('buyer_email') == user_email or t.get('seller_email') == user_email]
        return user_transactions
    
    return transactions

def create_sample_transactions(user_email):
    """Create sample transactions for demonstration"""
    transactions = [
        {
            'id': 1,
            'buyer_email': user_email,
            'seller_email': 'farmer1@example.com',
            'product_name': 'Maize',
            'quantity': 50,
            'price_per_kg': 2.10,
            'total_amount': 105.00,
            'status': 'completed',
            'payment_method': 'M-Pesa',
            'transaction_date': (datetime.now() - timedelta(days=2)).isoformat(),
            'delivery_date': (datetime.now() + timedelta(days=1)).isoformat()
        },
        {
            'id': 2,
            'buyer_email': user_email,
            'seller_email': 'farmer2@example.com',
            'product_name': 'Rice',
            'quantity': 25,
            'price_per_kg': 3.10,
            'total_amount': 77.50,
            'status': 'pending',
            'payment_method': 'Orange Money',
            'transaction_date': (datetime.now() - timedelta(hours=6)).isoformat(),
            'delivery_date': (datetime.now() + timedelta(days=3)).isoformat()
        }
    ]
    
    # Save to file
    os.makedirs("data", exist_ok=True)
    try:
        with open("data/transactions.json", 'w') as f:
            json.dump(transactions, f, indent=2)
    except:
        pass
    
    return transactions

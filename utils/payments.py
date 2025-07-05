import random
import json
import os
from datetime import datetime
import hashlib
import uuid

def process_mobile_payment(payment_method, phone_number, amount):
    """Process mobile money payment"""
    
    # Validate inputs
    if not phone_number or not amount or amount <= 0:
        return {
            'success': False,
            'message': 'Invalid payment details',
            'transaction_id': None
        }
    
    # Simulate payment processing
    success_rate = 0.9  # 90% success rate for simulation
    is_successful = random.random() < success_rate
    
    if is_successful:
        transaction_id = generate_transaction_id()
        
        # Log transaction
        transaction_data = {
            'transaction_id': transaction_id,
            'payment_method': payment_method,
            'phone_number': phone_number,
            'amount': amount,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }
        
        log_transaction(transaction_data)
        
        return {
            'success': True,
            'message': f'Payment of ${amount:.2f} processed successfully via {payment_method}',
            'transaction_id': transaction_id
        }
    else:
        # Simulate various failure reasons
        failure_reasons = [
            'Insufficient balance',
            'Network timeout',
            'Invalid phone number',
            'Service temporarily unavailable',
            'Transaction limit exceeded'
        ]
        
        return {
            'success': False,
            'message': random.choice(failure_reasons),
            'transaction_id': None
        }

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = str(int(datetime.now().timestamp()))
    random_part = str(random.randint(1000, 9999))
    return f"SAL{timestamp[-6:]}{random_part}"

def log_transaction(transaction_data):
    """Log transaction to file"""
    transactions_file = "data/payment_logs.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Load existing transactions or create empty list
    transactions = []
    if os.path.exists(transactions_file):
        try:
            with open(transactions_file, 'r') as f:
                transactions = json.load(f)
        except:
            transactions = []
    
    transactions.append(transaction_data)
    
    # Save to file
    try:
        with open(transactions_file, 'w') as f:
            json.dump(transactions, f, indent=2)
    except:
        pass

def get_payment_methods():
    """Get available payment methods for different regions"""
    return {
        'west_africa': [
            'Orange Money',
            'MTN Mobile Money',
            'Airtel Money',
            'Bank Transfer'
        ],
        'east_africa': [
            'M-Pesa',
            'Airtel Money',
            'MTN Mobile Money',
            'Bank Transfer'
        ],
        'north_africa': [
            'Bank Transfer',
            'CIB Wallet',
            'Fawry',
            'Orange Money'
        ],
        'southern_africa': [
            'EcoCash',
            'MTN Mobile Money',
            'Bank Transfer',
            'Airtel Money'
        ],
        'central_africa': [
            'Orange Money',
            'MTN Mobile Money',
            'Express Union Mobile',
            'Bank Transfer'
        ]
    }

def get_regional_payment_methods(location):
    """Get payment methods available for a specific location"""
    payment_methods = get_payment_methods()
    
    location_lower = location.lower()
    
    # Map locations to regions
    if any(country in location_lower for country in ['nigeria', 'ghana', 'senegal', 'mali', 'burkina', 'ivory']):
        return payment_methods['west_africa']
    elif any(country in location_lower for country in ['kenya', 'tanzania', 'uganda', 'ethiopia', 'rwanda']):
        return payment_methods['east_africa']
    elif any(country in location_lower for country in ['egypt', 'morocco', 'tunisia', 'algeria', 'libya']):
        return payment_methods['north_africa']
    elif any(country in location_lower for country in ['south africa', 'zimbabwe', 'botswana', 'zambia', 'namibia']):
        return payment_methods['southern_africa']
    elif any(country in location_lower for country in ['cameroon', 'gabon', 'chad', 'car', 'congo']):
        return payment_methods['central_africa']
    else:
        # Default to all methods
        all_methods = []
        for methods in payment_methods.values():
            all_methods.extend(methods)
        return list(set(all_methods))

def validate_phone_number(phone_number, payment_method):
    """Validate phone number format for specific payment method"""
    
    # Remove any spaces, hyphens, or parentheses
    clean_number = ''.join(filter(str.isdigit, phone_number))
    
    # Basic validation rules for different payment methods
    validation_rules = {
        'M-Pesa': {
            'prefixes': ['254'],
            'length': [12],
            'format': 'Country code + 9 digits'
        },
        'Orange Money': {
            'prefixes': ['221', '223', '226', '225'],
            'length': [11, 12],
            'format': 'Country code + 8-9 digits'
        },
        'MTN Mobile Money': {
            'prefixes': ['233', '256', '237', '234'],
            'length': [11, 12, 13],
            'format': 'Country code + 8-10 digits'
        },
        'Airtel Money': {
            'prefixes': ['234', '256', '254', '260'],
            'length': [11, 12, 13],
            'format': 'Country code + 8-10 digits'
        }
    }
    
    if payment_method in validation_rules:
        rules = validation_rules[payment_method]
        
        # Check length
        if len(clean_number) not in rules['length']:
            return False, f"Invalid number length. Expected format: {rules['format']}"
        
        # Check prefix
        if not any(clean_number.startswith(prefix) for prefix in rules['prefixes']):
            return False, f"Invalid country code. Expected format: {rules['format']}"
        
        return True, "Valid phone number"
    
    # For other payment methods, basic validation
    if len(clean_number) < 10 or len(clean_number) > 15:
        return False, "Phone number should be between 10-15 digits"
    
    return True, "Valid phone number"

def calculate_transaction_fee(amount, payment_method):
    """Calculate transaction fee based on payment method and amount"""
    
    fee_structures = {
        'M-Pesa': {
            'base_fee': 0.5,
            'percentage': 0.02,  # 2%
            'max_fee': 5.0
        },
        'Orange Money': {
            'base_fee': 0.3,
            'percentage': 0.015,  # 1.5%
            'max_fee': 4.0
        },
        'MTN Mobile Money': {
            'base_fee': 0.4,
            'percentage': 0.018,  # 1.8%
            'max_fee': 4.5
        },
        'Airtel Money': {
            'base_fee': 0.3,
            'percentage': 0.016,  # 1.6%
            'max_fee': 4.2
        },
        'Bank Transfer': {
            'base_fee': 1.0,
            'percentage': 0.005,  # 0.5%
            'max_fee': 10.0
        }
    }
    
    if payment_method in fee_structures:
        fee_structure = fee_structures[payment_method]
        calculated_fee = fee_structure['base_fee'] + (amount * fee_structure['percentage'])
        return min(calculated_fee, fee_structure['max_fee'])
    
    # Default fee for unknown payment methods
    return amount * 0.02  # 2% default fee

def get_transaction_status(transaction_id):
    """Get the status of a transaction"""
    transactions_file = "data/payment_logs.json"
    
    if not os.path.exists(transactions_file):
        return None
    
    try:
        with open(transactions_file, 'r') as f:
            transactions = json.load(f)
    except:
        return None
    
    for transaction in transactions:
        if transaction.get('transaction_id') == transaction_id:
            return transaction
    
    return None

def refund_transaction(transaction_id, reason=""):
    """Process a refund for a transaction"""
    transaction = get_transaction_status(transaction_id)
    
    if not transaction:
        return {
            'success': False,
            'message': 'Transaction not found'
        }
    
    if transaction.get('status') != 'completed':
        return {
            'success': False,
            'message': 'Only completed transactions can be refunded'
        }
    
    # Simulate refund processing
    refund_successful = random.random() < 0.95  # 95% success rate
    
    if refund_successful:
        refund_data = {
            'refund_id': generate_transaction_id(),
            'original_transaction_id': transaction_id,
            'amount': transaction['amount'],
            'reason': reason,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }
        
        # Log refund
        log_refund(refund_data)
        
        return {
            'success': True,
            'message': f'Refund of ${transaction["amount"]:.2f} processed successfully',
            'refund_id': refund_data['refund_id']
        }
    else:
        return {
            'success': False,
            'message': 'Refund processing failed. Please contact customer support.'
        }

def log_refund(refund_data):
    """Log refund to file"""
    refunds_file = "data/refund_logs.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Load existing refunds or create empty list
    refunds = []
    if os.path.exists(refunds_file):
        try:
            with open(refunds_file, 'r') as f:
                refunds = json.load(f)
        except:
            refunds = []
    
    refunds.append(refund_data)
    
    # Save to file
    try:
        with open(refunds_file, 'w') as f:
            json.dump(refunds, f, indent=2)
    except:
        pass

def generate_payment_qr_code(payment_method, phone_number, amount):
    """Generate QR code data for mobile payments"""
    
    qr_data = {
        'payment_method': payment_method,
        'merchant_id': 'SAMA_AGROLINK',
        'phone_number': phone_number,
        'amount': amount,
        'currency': 'USD',
        'transaction_ref': generate_transaction_id(),
        'timestamp': datetime.now().isoformat()
    }
    
    # Create QR code string (in real implementation, this would generate actual QR code)
    qr_string = json.dumps(qr_data)
    
    return {
        'qr_data': qr_string,
        'display_text': f"Scan to pay ${amount:.2f} via {payment_method}",
        'expiry_minutes': 15
    }

def verify_payment_security(phone_number, amount, otp_code=None):
    """Verify payment security measures"""
    
    security_checks = {
        'phone_verified': True,  # Assume phone is verified
        'amount_valid': 0.01 <= amount <= 10000,  # Amount limits
        'otp_valid': True,  # In real implementation, verify actual OTP
        'fraud_check': random.random() > 0.05  # 5% chance of fraud detection
    }
    
    all_checks_passed = all(security_checks.values())
    
    return {
        'security_passed': all_checks_passed,
        'checks': security_checks,
        'risk_level': 'low' if all_checks_passed else 'high'
    }

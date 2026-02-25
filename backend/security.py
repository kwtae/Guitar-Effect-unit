import jwt
from datetime import datetime, timedelta

# Secret key for encoding and decoding JWT
SECRET_KEY = "your_secret_key"

# Function to generate JWT token

def create_token(data):
    token = jwt.encode({
        'user': data,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')
    return token

# Function to decode JWT token

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

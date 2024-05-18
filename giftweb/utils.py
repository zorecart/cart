import base64
from django.conf import settings

def encode_id(id):
    """Encode the ID using Base64 encoding."""
    return base64.urlsafe_b64encode(str(id).encode()).decode()

def decode_id(encoded_id):
    """Decode the ID from Base64 encoding."""
    return int(base64.urlsafe_b64decode(encoded_id.encode()).decode())

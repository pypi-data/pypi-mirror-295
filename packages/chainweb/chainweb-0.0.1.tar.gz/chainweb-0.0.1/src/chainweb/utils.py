import json
from base64 import urlsafe_b64decode, urlsafe_b64encode

# ############################################################################ #
# Base64 Encoding/Decoding
#
# In chainweb only the urlsafe variant of base64 is used with padding stripped.

def decode_base64(s):
    """Decode a base64 urlsafe (without padding) encoded bytes or string."""
    return urlsafe_b64decode(s + '===')

def encode_base64(b):
    """Encode a bytes object to a base64 urlsafe (without padding) encoded string."""
    return urlsafe_b64encode(b).decode('UTF-8').strip('=')

def encode_base64_bytes(b):
    """Encode a bytes object to a base64 urlsafe (without padding) encoded bytes."""
    return urlsafe_b64encode(b).rstrip(b'=')

# ############################################################################ #
# JSON

def json_decode_bytes(b: bytes | bytearray) -> dict:
    """Decode a JSON encoded bytes object to a dictionary."""
    return json.loads(b.decode('utf-8'))

def json_dict_from_b64(b: str) -> dict:
    """Decode a base64 urlsafe (without padding) encoded string to a dictionary."""
    return json_decode_bytes(decode_base64(b))
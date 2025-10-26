import hashlib
import uuid
import string

# Define the Base62 alphabet
ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase
BASE = len(ALPHABET)  # 62

def to_base62(num: int) -> str:
    """Convert a large integer to a Base62 string."""
    if num == 0:
        return ALPHABET[0]
    chars = []
    while num > 0:
        num, rem = divmod(num, BASE)
        chars.append(ALPHABET[rem])
    return ''.join(reversed(chars))

def generate_short_code_from_uuid(link_url: str, length: int = 8) -> str:
    """Generate a short, Base62-encoded hash for a given link."""
    # Add random salt for uniqueness (even if same URL repeats)
    random_salt = str(uuid.uuid4())
    # Hash URL + salt to get a consistent-length digest
    hash_bytes = hashlib.sha256((str(link_url) + random_salt).encode()).digest()
    # Convert hash bytes to a large integer
    hash_int = int.from_bytes(hash_bytes, "big")
    # Convert integer to Base62
    base62_code = to_base62(hash_int)
    # Truncate to desired length
    return base62_code[:length]

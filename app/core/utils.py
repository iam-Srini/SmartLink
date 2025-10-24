import hashlib
import uuid

def generate_short_code_from_uuid(link_url: str, length: int=8):
    random_salt = str(uuid.uuid4())
    hash_val = hashlib.sha256(link_url.encode() + random_salt).hexdigest()
    return hash_val[:length]


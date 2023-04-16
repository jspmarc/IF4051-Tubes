from hashlib import sha3_512
from typing import Any, Dict

BASE_RESPONSE: Dict[int | str, Dict[str, Any]] = {
    401: {"message": "X-Token is invalid."},
}


def hash(unhashed: str):
    """
    For now, we are using SHA-512
    """
    return sha3_512(unhashed.encode("utf-8")).hexdigest()

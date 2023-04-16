from hashlib import sha3_512
from typing import Any, Dict
"""
For now use SHA-512
"""

BASE_RESPONSE: Dict[int | str, Dict[str, Any]] = {
    401: {
        "message": "X-Token is invalid."
    },
}


def hash(unhashed: str):
    return sha3_512(unhashed.encode("utf-8")).hexdigest()

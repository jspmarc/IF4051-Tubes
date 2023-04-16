from hashlib import sha3_512


def hash(unhashed: str):
    """
    For now, we are using SHA-512
    """
    return sha3_512(unhashed.encode("utf-8")).hexdigest()

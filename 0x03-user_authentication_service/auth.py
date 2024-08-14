#!/usr/bin/env python3
"""
User Authentication Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password with a salt using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

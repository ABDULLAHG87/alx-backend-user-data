#!/usr/bin/env python3
"""
Script for Password Encryption and Validation
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Function that generated a hash_password"""
    encode = password.encode()
    hashed = bycrypt.hashpw(encoded, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function to validate the password matched"""
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid

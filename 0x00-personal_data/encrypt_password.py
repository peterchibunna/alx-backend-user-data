#!/usr/bin/env python3
"""
Module 0x00. Personal data
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """User passwords should NEVER be stored in plain text in a database
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed

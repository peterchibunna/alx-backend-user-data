#!/usr/bin/env python3
"""
Module:
4. Hash password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """The returned bytes is a salted hash of the input password,
    hashed with `bcrypt.hashpw`
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

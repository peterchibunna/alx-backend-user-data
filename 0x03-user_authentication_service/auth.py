#!/usr/bin/env python3
"""
Module:
4. Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """The returned bytes is a salted hash of the input password,
    hashed with `bcrypt.hashpw`
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Init Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a User
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            db_password = _hash_password(password)
            user = self._db.add_user(email, str(db_password))
            return user
        raise ValueError("User {} already exists".format(email))

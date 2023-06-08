#!/usr/bin/env python3
"""
Module:
4. Hash password
"""
from typing import Union

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """The returned bytes is a salted hash of the input password,
    hashed with `bcrypt.hashpw`
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID.
    """
    return str(uuid4())


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
            user = self._db.add_user(email, db_password)
            return user
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """8. Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf8'), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """10. Get session ID
        In this task, you will implement the Auth.create_session method. It
        takes an email string argument and returns the session ID as a string.
        The method should find the user corresponding to the email, generate
        a new UUID and store it in the database as the user’s session_id,
        then return the session ID. Remember that only public methods of
        self._db can be used.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                return None
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """12. Find user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

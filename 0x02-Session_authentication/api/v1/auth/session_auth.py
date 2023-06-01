#!/usr/bin/env python3
"""The SessionAuth: class
"""
import base64
import uuid
from typing import TypeVar
from models.user import User

from .auth import Auth


class SessionAuth(Auth):
    """Main SessionAuth that inherits from the Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session
        """
        if user_id is None:
            return None
        if user_id is not None and type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

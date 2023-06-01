#!/usr/bin/env python3
"""The SessionAuth: class
"""
import os

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
        if user_id is None or user_id is not None and type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """6. Use Session ID for identifying a User
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id=session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """8. Logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        try:
            self.user_id_by_session_id.pop(session_id, None)
            return True
        except KeyError:
            return False

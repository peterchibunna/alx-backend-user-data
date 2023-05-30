#!/usr/bin/env python3
"""The Auth: class
"""
from flask import request
from models.user import User
from typing import List, TypeVar


class Auth:
    """Main auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Should we require auth?
        """
        return False

    def authorization_header(self, request=None) -> str:
        """This should be the header?
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user of the request?
        """

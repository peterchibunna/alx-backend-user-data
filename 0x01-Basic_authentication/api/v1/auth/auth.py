#!/usr/bin/env python3
"""The Auth: class
"""
from flask import request
from models.user import User
from typing import List, TypeVar


def pathify(path):
    """Returns a correctly slashed pathname
    """
    return path if path.endswith('/') else '{}/'.format(path)


class Auth:
    """Main auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Should we require auth?
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if pathify(path) in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """This should be the header?
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user of the request?
        """

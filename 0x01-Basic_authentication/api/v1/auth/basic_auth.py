#!/usr/bin/env python3
"""The BasicAuth: class
"""
import base64

from .auth import Auth


class BasicAuth(Auth):
    """Main BasicAuth that inherits from the Auth class
    """

    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """return the Base64 part of the authorization header for a Basic
        Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic'):
            return None
        else:
            try:
                return authorization_header.split('Basic ')[1]
            except Exception:
                return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the value of the decoded base64 part
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(base64_authorization_header,
                                    validate=True).decode('utf-8')
        except Exception:
            return None

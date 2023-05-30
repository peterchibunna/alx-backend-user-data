#!/usr/bin/env python3
"""The BasicAuth: class
"""
import base64
from typing import TypeVar
from models.user import User

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
            return base64.b64decode(
                base64_authorization_header, validate=True).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """9. Basic - User credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None,)
        if type(decoded_base64_authorization_header) != str:
            return (None, None,)
        a = decoded_base64_authorization_header.split(":")
        if len(a) != 2:
            return (None, None,)
        return tuple(a)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Simple document
        """
        if user_email is None or type(user_email) != str or user_pwd is None \
                or type(user_pwd) != str:
            return None
        else:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """gets current user
        """
        header = self.authorization_header(request)
        auth_token = self.extract_base64_authorization_header(header)
        auth_token = self.decode_base64_authorization_header(auth_token)
        credentials = self.extract_user_credentials(auth_token)
        email = credentials[0]
        password = credentials[1]
        return self.user_object_from_credentials(email, password)

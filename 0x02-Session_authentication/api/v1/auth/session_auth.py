#!/usr/bin/env python3
"""The SessionAuth: class
"""
import base64
from typing import TypeVar
from models.user import User

from .auth import Auth


class SessionAuth(Auth):
    """Main SessionAuth that inherits from the Auth class
    """

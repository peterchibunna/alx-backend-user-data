#!/usr/bin/env python3
"""9. Expiration?
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """

    def __init__(self):
        """Initializes a SessionExpAuth instance
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session id
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str or session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieves the user id of the user from the session id
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if session_id in self.user_id_by_session_id:
            session_data = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_data['user_id']
            if 'created_at' not in session_data:
                return None
            now = datetime.now()
            session_duration = timedelta(seconds=self.session_duration)
            if session_data['created_at'] + session_duration < now:
                return None
            return session_data['user_id']

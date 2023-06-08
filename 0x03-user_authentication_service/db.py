#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base, User

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds and returns the added User
        """
        try:
            u = User(email=email, hashed_password=hashed_password)
            self._session.add(u)
            self._session.commit()
            return u
        except Exception:
            self._session.rollback()
            return None

    def find_user_by(self, **kwargs) -> User:
        """Finds a user
        """
        attributes = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                attributes[key] = value
            else:
                raise InvalidRequestError()
        results = self._session.query(User).filter_by(**attributes)
        if results.count() == 0:
            raise NoResultFound()

        if results.first() is None:
            raise NoResultFound()
        return results.first()

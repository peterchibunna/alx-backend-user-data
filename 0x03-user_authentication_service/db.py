#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy import exc as exception

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
        # attributes = {}
        # for key, value in kwargs.items():
        #     if hasattr(User, key):
        #         attributes[key] = value
        #     else:
        #         raise exception.InvalidRequestError()
        #
        # result = self._session.query(User).filter_by(**attributes).first()
        # if result is None:
        #     raise exception.NoResultFound()
        # return result
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise exception.InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise exception.NoResultFound()
        return result

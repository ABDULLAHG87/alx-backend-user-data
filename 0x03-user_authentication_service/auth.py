#!/usr/bin/env python3
"""Authorization Module"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> str:
    """Function to hash password in authentication"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid():
    """Function for generating uuid"""
    id = uuid4()
    return str(id)

class Auth:
    """Definition of Authorization Class"""

    def __init__(self):
        """Initialization Method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """Method for regsitering User"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creating Session for email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

#!/usr/bin/env python3
"""Module for session authentication"""

from models.user import User
from uuid import uuid4
from .auth import Auth


class SessionAuth(Auth):
    """Class definition for Session Authentication"""
    user_id_by_session_id = {}

    def session_cookie(self, request):
        """Retrieve Session Cookies from a request"""
        if request is None:
            return None
        return request.cookies.get('session_id')

    def create_session(self, user_id: str = None) -> str:
        """Method for creating session"""
        if user_id is None or not isinstance(user_id, str):
            return None

        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method for creating session id for user """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Method for tracking current user"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Method for destroying session cookie"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True

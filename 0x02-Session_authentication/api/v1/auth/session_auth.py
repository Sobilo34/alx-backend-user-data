#!/usr/bin/env python3
"""A create a class to manage the API session authentication"""
import os
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from base64 import b64decode
from models.user import User
from flask import request
from uuid import uuid4


class SessionAuth(Auth):
    """A session authentication class"""
    user_id_by_session_id = {}

    def __init__(self):
        """Initialize the SessionAuth class"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        An instance method that creates a Session ID for a user_id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        An instance method that returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
        This returns a User instance based on a cookie value
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        deletes the user session / logout
        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False

        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_cookie]
        return True

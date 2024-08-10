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

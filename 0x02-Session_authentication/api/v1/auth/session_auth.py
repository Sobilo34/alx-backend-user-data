#!/usr/bin/env python3
"""A create a class to manage the API session authentication"""
import os
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from base64 import b64decode
from models.user import User
from flask import request


class SessionAuth(Auth):
    """A session authentication class"""
    def __init__(self):
        """Initialize the SessionAuth class"""
        super().__init__()

    # Add your implementation here

#!/usr/bin/env python3
"""A create a class to manage the API authentication"""
from flask import request
from typing import List, TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """A class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """A function that returns the Base64 part of
        the Authorization header for a Basic Authentication
        """
        if authorization_header is None or type(
                authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

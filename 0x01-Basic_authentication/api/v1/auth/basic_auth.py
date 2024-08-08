#!/usr/bin/env python3
"""A create a class to manage the API authentication"""
from flask import request
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """A function that returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or type(
                base64_authorization_header) is not str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """A function that returns the user email
        and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None or type(
                decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

#!/usr/bin/env python3
"""A create a class to manage the API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A method that requires authentication"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith(
                    '*') and path.startswith(excluded_path[:-1]):
                return False
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """A method that return the value of the header request"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """A method that return None"""
        return None

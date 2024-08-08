#!/usr/bin/env python3
"""A create a class to manage the API authentication"""
from flask import request
from typing import List, TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """A class BasicAuth that inherits from Auth"""
    pass

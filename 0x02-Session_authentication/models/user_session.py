#!/usr/bin/env python3

""" UserSession module for the API
"""

from models.base import Base
from datetime import datetime


class UserSession(Base):
    """
    This is the UserSession model that inherits from Base
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize the UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

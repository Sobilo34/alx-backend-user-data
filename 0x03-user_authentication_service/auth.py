#!/usr/bin/env python3
"""
User Authentication Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes a password with a salt using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    """
    Generates a Universally Unique Identifier (UUID).
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user if the user doesn't already exist.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            _hash_password(password)
            return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a login is valid.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.

        Raises:
            None
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets the user corresponding to the session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The user corresponding to the session ID.

        Raises:
            None
        """
        try:
            if session_id is None:
                return None
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session for the user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None

        Raises:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Gets a reset password token for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user doesn't exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password using a reset token.

        Args:
            reset_token (str): The reset password token.
            password (str): The new password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
            return None
        except Exception:
            raise ValueError()

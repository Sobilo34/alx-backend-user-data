#!/usr/bin/env python3
"""
End to End Integration Test
"""
import requests

# Constants
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Test user registration.
    """
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with an incorrect password.
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test user login and return the session ID.
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    # Return session_id from cookies
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """
    Test access to profile when the user is not logged in.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test access to profile when the user is logged in.
    """
    response = requests.get(
        f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """
    Test user logout.
    """
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}
    profile_unlogged()


def reset_password_token(email: str) -> str:
    """
    Request a password reset token and return it.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    token = response.json().get("reset_token")
    assert token is not None
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test password update using the reset token.
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    # Integration test flow
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()

    # Login and test profile access
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)

    # Logout and reset password
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)

    # Update password and verify login with new password
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

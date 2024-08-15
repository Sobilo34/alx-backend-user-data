#!/usr/bin/env python3
"""
The flask app
"""
from flask import Flask, request
from flask import jsonify, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def my_form():
    """A method that retuns the JSON response of a form
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """Register a user
    """
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify(email=user.email, message='user created'), 200
    except ValueError:
        return jsonify(message="email already registered"), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Handle the POST request to create a new session (login)."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Email and password are required")

    if AUTH.valid_login(email=email, password=password):
        session_id = AUTH.create_session(email=email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401, description="Invalid login")


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Handle the DELETE request to destroy a session (logout)."""
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403, description="No session cookie found")

    user = AUTH.get_user_from_session_id(session_id=session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403, description="Session not valid")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Handle the GET request to retrieve user profile."""
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403, description="No session cookie found")

    user = AUTH.get_user_from_session_id(session_id=session_id)

    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403, description="Invalid session")


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Handle the POST request to generate a reset password token."""
    email = request.form.get('email')

    if not email:
        abort(400, description="Email is required")

    try:
        token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403, description="Unable to generate reset token")


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Handle the PUT request to update the password."""
    email = request.form.get('email')
    token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not token or not new_password:
        abort(400, description="Email, token, and new password are required")

    try:
        AUTH.update_password(reset_token=token, password=new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403, description="Invalid reset token")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

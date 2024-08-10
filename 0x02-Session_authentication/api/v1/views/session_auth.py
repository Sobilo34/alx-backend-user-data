#!/usr/bin/env python3
""" Module of Session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Handles User login
    Return:
      - User object JSON represented
      - 400 if the User ID doesn't exist
    """
    # Retrieve email and password from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing or empty
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    user = User.search({'email': email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    # Create a Session ID for the User ID
    session_id = auth.create_session(user.id)

    # Generate the response
    response = make_response(jsonify(user.to_json()))

    # Set the session ID in the cookie
    session_name = getenv("SESSION_NAME", "session_id")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Delete user and logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)

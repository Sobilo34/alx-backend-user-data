#!/usr/bin/env python3
"""
The flask app
"""
from flask import Flask, request
from flask import jsonify
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

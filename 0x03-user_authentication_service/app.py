#!/usr/bin/env python3
"""
The flask app
"""
from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def my_form():
    """A method that retuns the JSON response of a form
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

#!/usr/bin/env python3
"""Module:
Flask Application
"""
# from typing import Any, Tuple

from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def bienvenue() -> str:
    """The home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def post_users() -> str:
    """Register user route
    """
    from auth import Auth
    AUTH = Auth()
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

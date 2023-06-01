#!/usr/bin/env python3
"""Module of session authenticating views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """7. New view for Session Authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    user_not_found = {"error": "no user found for this email"}

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(user_not_found), 404
    if len(users) <= 0:
        return jsonify(user_not_found), 404
    u = users[0]
    if u.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(u, 'id'))
        response = jsonify(u.to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """8. Logout
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})

#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE", None)
if auth_type == "auth":
    auth = Auth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Forbidden"}), 403


a, b, c, d = '/api/v1/status/', '/api/v1/unauthorized/', \
    '/api/v1/forbidden/', \
    '/api/v1/auth_session/login/'


@app.before_request
def check_authentication():
    """Check if we must require authentication for a user or not
    """
    if auth is not None:
        if auth.require_auth(request.path, [a, b, c, d]):
            auth_header = auth.authorization_header(request)
            user = auth.current_user(request)
            cookie = auth.session_cookie(request)
            request.current_user = user
            if auth_header is None and cookie is None:
                abort(401)
            if user is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")

    app.run(host=host, port=port)

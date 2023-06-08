#!/usr/bin/env python3
"""Module:
Flask Application
"""
from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def bienvenue() -> str:
    """The home page
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

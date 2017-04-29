#!/usr/bin/python3
"""API for the AirBnB clone application"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Close API session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"))

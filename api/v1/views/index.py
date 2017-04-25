#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Number of objects for each model"""
    stats = {}
    for k, v in storage._DBStorage__models_available.items():
        stats[v.__tablename__] = storage.count(k)
    return jsonify(stats)

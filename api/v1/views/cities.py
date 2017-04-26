#!/usr/bin/python3
"""API functionality for City objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities(state_id):
    """
    Return a JSON list of all City objects for a given State.
    """
    try:
        state = storage.get('State', state_id)
    except:
        abort(404)
    cities = [city.to_json() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Return a City object given it's ID."""
    try:
        city = storage.get("City", city_id)
    except:
        abort(404)
    return jsonify(city.to_json())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object by it's ID."""
    try:
        city = storage.get("City", city_id)
        storage.delete(city)
        storage.save()
    except:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """Add a new City object to a State."""
    try:
        r = request.get_json()
    if not request.is_json:
        abort(400, {"error": "Not a JSON"})
    if 'name' not in r.keys():
        abort(400, {"error": "Missing name"})
    state = State(name=r['name'])
    state.save()
    return jsonify(state.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City object."""
    s = storage.get("State", state_id)
    if not s:
        abort(404)
    r = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")
    s = s.to_json()
    keys = ['id', 'created_at', 'updated_at']
    s.update({k: v for (k, v) in r.items() if k not in keys})
    storage.save()
    return jsonify(s), 200

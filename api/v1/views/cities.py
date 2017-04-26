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
    except:
        return jsonify("Not a JSON"), 400
    if 'name' not in r.keys():
        abort(400, {"Missing name"})
    city = City(name=r['name'])
    city.save()
    return jsonify(city.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City object."""
    try:
        city = storage.get("City", city_id)
    except:
        return not_found(404)
    if request.is_json is False:
        abort(400, {"Not a JSON"})

    city = city.to_json()
    keys = ['id', 'state_id', 'created_at', 'updated_at']
    city.update({k: v for (k, v) in r.items() if k not in keys})
    city.save()
    return jsonify(city), 200


@app.errorhandler(404)
def not_found(error):
    """Handle HTTP error code 404."""
    return jsonify(error="Not found"), 404

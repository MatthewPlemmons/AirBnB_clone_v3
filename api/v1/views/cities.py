#!/usr/bin/python3
"""API functionality for City objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities(state_id):
    """
    Return a JSON list of all City objects for a given State.
    """
    try:
        state = storage.get('State', state_id)
        return jsonify([city.to_json() for city in state.cities]), 200
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Return a City object given it's ID."""
    try:
        city = storage.get("City", city_id).to_json()
    except:
        abort(404)
    return jsonify(city), 200


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
    r = request.get_json()
    if r is None:
        return jsonify(error='Not a JSON'), 400
    if storage.get('State', state_id) is None:
        abort(404)
    try:
        city = City(name=r['name'])
        city.state_id = state_id
        city.save()
    except:
        return jsonify(error='Missing name'), 400
    return jsonify(city.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City object."""
    try:
        r = request.get_json().items()
    except:
        return jsonify(error='Not a JSON'), 400
    try:
        city = storage.get('City', city_id)
        keys = ['id', 'state_id', 'created_at', 'updated_at']
        {setattr(city, k, v) for k, v in r if k not in keys}
        city.save()
    except:
        abort(404)
    return jsonify(city.to_json()), 200

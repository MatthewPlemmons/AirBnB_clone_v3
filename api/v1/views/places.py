#!/usr/bin/python3
"""API functionality for Place objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.places import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def all_places():
    """Return a JSON list of all Place objects in a given City."""
    try:
        city = storage.get('City', city_id)
        return jsonify([place.to_json() for place in city.places])
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Return a Place object given it's ID."""
    try:
        place = storage.get("Place", place_id)
        return jsonify(place.to_json())
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object by it's ID."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def add_place(city_id):
    """Add a new Place object to a given City."""
    if storage.get('City', city_id) is None:
        abort(404)
    r = request.get_json()
    if r is None:
        return jsonify(error='Not a JSON'), 400
    if 'user_id' not in r:
        return jsonify(error='Missing user_id'), 400
    if 'name' not in r:
        return jsonify(error='Missing name'), 400
    place = Place(**r)
    place.save()
    return jsonify(place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place object."""
    try:
        r = request.get_json().items()
    except:
        return jsonify(error='Not a JSON'), 400
    try:
        place = storage.get('Place', place_id)
        {setattr(place, k, v) for k, v in r if k not in
         ['id', 'user_id', 'city_id', 'created_at', 'updated_at']}
        place.save()
    except:
        abort(404)
    return jsonify(place.to_json()), 200

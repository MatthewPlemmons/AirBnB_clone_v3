#!/usr/bin/python3
"""API functionality for City objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def all_amenities():
    """
    Return a JSON list of all Amenity objects.
    """
    try:
        amenities = storage.all('Amenity').values()
    except:
        abort(404)
    a = [amenity.to_json() for amenity in amenities]
    return jsonify(a)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Return an Amenity object given it's ID."""
    try:
        amenity = storage.get("Amenity", amenity_id)
    except:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an Amenity object by it's ID."""
    try:
        amenity = storage.get("Amenity", amenity_id)
        storage.delete(amenity)
        storage.save()
    except:
        abort(404)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def add_amenity():
    """Add a new Amenity object."""
    try:
        r = request.get_json()
    except:
        return jsonify("Not a JSON"), 400
    if 'name' not in r.keys():
        abort(400, {"Missing name"})
    amenity = Amenity(name=r['name'])
    amenity.save()
    return jsonify(amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an Amenity object."""
    try:
        amenity = storage.get("Amenity", amenity_id)
    except:
        abort(404)
    if request.is_json is False:
        abort(400, {"Not a JSON"})
    r = request.get_json()
    amenity = amenity.to_json()
    keys = ['id', 'created_at', 'updated_at']
    amenity.update({k: v for (k, v) in r.items() if k not in keys})
    storage.save()
    return jsonify(amenity), 200

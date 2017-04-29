#!/usr/bin/python3
"""API functionality for Amenity objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
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
        return jsonify(amenity.to_json())
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an Amenity object by it's ID."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def add_amenity():
    """Add a new Amenity object."""
    try:
        r = request.get_json()
        amenity = Amenity(name=r['name'])
        amenity.save()
    except KeyError:
        return jsonify(error="Missing name"), 400
    except:
        return jsonify(error="Not a JSON"), 400
    return jsonify(amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an Amenity object."""
    try:
        r = request.get_json().items()
    except:
        return jsonify(error="Not a JSON"), 400
    try:
        amenity = storage.get('Amenity', amenity_id)
        {setattr(amenity, k, v) for k, v in r if k not in
         ['id', 'created_at', 'updated_at']}
        amenity.save()
    except:
        abort(404)
    return jsonify(amenity.to_json()), 200

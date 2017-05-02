#!/usr/bin/python3
"""API functionality for Amenity objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.amenity import Amenity
from models.place import Place
from os import getenv


#if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':

@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def amenities_of_place(place_id):
    """Return a JSON list of all Amenity objects of a given Place."""
    try:
        place = storage.get('Place', place_id)
        return jsonify([amenity.to_json() for amenity in place.amenities])
    except:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_from(place_id, amenity_id):
    """Delete an Amenity object by it's ID."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    try:
        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to(place_id, amenity_id):
    """Link an Amenity object to a given Place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        a = {a.to_json() for a in place.amenities if a == amenity}
        return jsonify(a), 200
    try:
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_json()), 201
    except:
        abort(404)

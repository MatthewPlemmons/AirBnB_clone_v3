#!/usr/bin/python3
"""API functionality for Place objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.place import Place
import itertools


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def all_places(city_id):
    """Return a JSON list of all Place objects in a given City."""
    try:
        city = storage.get('City', city_id)
        return jsonify([place.to_json() for place in city.places])
    except:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """Return a Place object given it's ID."""
    try:
        place = storage.get("Place", place_id)
        return jsonify(place.to_json())
    except:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object by it's ID."""
    try:
        storage.delete(storage.get('Place', place_id))
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


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
    place.city_id = city_id
    place.save()
    return jsonify(place.to_json()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
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


@app_views.route('/places_search', strict_slashes=False,
                 methods=['POST'])
def places_search():
    """Search for all Places linked to given objects."""
    places = []
    r = request.get_json()

    if 'amenities' in r:
        a = [storage.get('Amenity', amenity) for amenity in r['amenities']]
        for i in a:
            p = i.place_amenities
            place_id = p[0].place_id
            place = storage.get('Place', place_id)
            n = 0
            for a in place.amenities:
                if a.id not in r['amenities']:
                    break
                ++n
                if n == len(r['amenities']):
                    places.append(place)

    # Gather place objects from states
    if 'states' in r:
        state_ids = r['states']
        states = [storage.get('State', state) for state in state_ids]
        cities = [state.cities for state in states]
        cities = list(itertools.chain.from_iterable(cities))
        for city in cities:
            if city.places:
                places.append(city.places)

    # Gather place objects from cities
    if 'cities' in r:
        for city in r['cities']:
            c = storage.get('City', city)
            if c not in cities:
                places.append(c.places)

    del places[0][0].amenities
    return jsonify([places[0][0].to_json()])

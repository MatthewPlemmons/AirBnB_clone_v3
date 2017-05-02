#!/usr/bin/python3
"""API functionality for Review objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def all_reviews(place_id):
    """Return a JSON list of all Review objects for a given Place."""
    try:
        place = storage.get('Place', place_id)
        return jsonify([review.to_json() for review in place.reviews])
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """Return a Review object given it's ID."""
    try:
        review = storage.get('Review', review_id)
        return jsonify(review.to_json())
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review object by it's ID."""
    try:
        storage.delete(storage.get('Review', review_id))
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def add_review(place_id):
    """Add a new Review object to a given Place."""
    if storage.get('Place', place_id) is None:
        abort(404)
    r = request.get_json()
    if r is None:
        return jsonify(error='Not a JSON'), 400
    if 'user_id' not in r:
        return jsonify(error='Missing user_id'), 400
    if 'text' not in r:
        return jsonify(error='Missing text'), 400
    review = Review(**r)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Update a Review object."""
    try:
        r = request.get_json().items()
    except:
        return jsonify(error='Not a JSON'), 400
    try:
        review = storage.get('Review', review_id)
        {setattr(review, k, v) for k, v in r if k not in
         ['id', 'user_id', 'place_id', 'created_at', 'updated_at']}
        review.save()
        return jsonify(review.to_json()), 200
    except:
        abort(404)

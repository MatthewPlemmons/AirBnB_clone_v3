#!/usr/bin/python3
"""API functionality for User objects."""
from api.v1.views import app_views, storage
from flask import abort, request, jsonify
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """
    Return a JSON list of all User objects.
    """
    try:
        users = storage.all('User').values()
    except:
        abort(404)
    return jsonify([user.to_json() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Return a User object given it's ID."""
    try:
        user = storage.get("User", user_id)
        return jsonify(user.to_json())
    except:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a User object by it's ID."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user():
    """Add a new User object."""
    try:
        r = request.get_json()
        if 'email' not in r:
            return jsonify(error='Missing email'), 400
        if 'password' not in r:
            return jsonify(error='Missing password'), 400
        user = User(first_name=r['name'],
                    last_name=r['last'],
                    email=r['email'],
                    password=r['password'])
        user.save()
    except KeyError:
        return jsonify(error="Missing name"), 400
    except:
        return jsonify(error="Not a JSON"), 400
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an User object."""
    try:
        r = request.get_json().items()
    except:
        return jsonify(error="Not a JSON"), 400
    try:
        user = storage.get('User', user_id)
        {setattr(user, k, v) for k, v in r if k not in
         ['id', 'email', 'created_at', 'updated_at']}
        user.save()
    except:
        abort(404)
    return jsonify(user.to_json()), 200

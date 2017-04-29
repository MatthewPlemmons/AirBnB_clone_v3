#!/usr/bin/python3
"""API functionality for State objects"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models.base_model import BaseModel
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Return a JSON list of all State objects"""
    state_list = []
    states = storage.all('State').values()
    for s in states:
        state_list.append(s.to_json())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_by_id(state_id):
    """Return or delete a State object depending on HTTP method"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    if request.method == "GET":
        return jsonify(s.to_json())
    else:
        storage.delete(s)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def new_state():
    """Create a new State object"""
    r = request.get_json()
    if not request.is_json:
        abort(400, {"error": "Not a JSON"})
    if 'name' not in r.keys():
        abort(400, {"error": "Missing name"})
    state = State(name=r['name'])
    state.save()
    return jsonify(state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a State object"""
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

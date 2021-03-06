from flask import Blueprint, request, jsonify


events_bp = Blueprint('events', __name__, url_prefix='/api/events/')

from .utils import save_events, get_events, delete_events

@events_bp.route('', methods=["POST"])
def add_events():
    """ This function is used to get the request for adding events to the database
    """
    data = request.get_json()
    description = data.get('description')
    time = data.get('time')
    location = data.get('location')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank) or (not time) or (not location):
        return jsonify(result={'failed_msg': "Unanle to save events with missing fields"})

    return jsonify(result=save_events(title, description, rank, time, location, latitude, longitude))


@events_bp.route('', methods=["PUT"])
def update_events():
    """ This function is used to get the request for adding events to the database
    """
    data = request.get_json()
    description = data.get('description')
    title = data.get('title')
    time = data.get('time')
    location = data.get('location')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    rank = data.get('rank')
    events_id = data.get('id')

    if  (not title) or (not description) or (not rank) or (not time) or (not location) or (not events_id):
        return jsonify(result={'failed_msg': "Unable to save events with missing fields"})

    return jsonify(result=save_events(title, description, rank, time, location, latitude, longitude, _id=events_id))


@events_bp.route('', methods=['GET'])
def get_events_data():
    """ This function is used to gets all number of specified events items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_events(maximum=maxim))


@events_bp.route('', methods=['DELETE'])
def delete_events_data():
    """ This function is used to delete a particular events item """
    data = request.args
    events_id = data.get('id')
    results, status_code = delete_events(events_id)
    return jsonify(result=results), status_code
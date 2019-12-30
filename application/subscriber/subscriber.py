from flask import Blueprint, request, jsonify


subscriber_bp = Blueprint('subscriber', __name__, url_prefix='/api/subscriber/')

from .utils import save_subscriber, delete_subscriber, get_subscribers

@subscriber_bp.route('', methods=["POST"])
def add_subscribers():
    """ This function is used to get the request for adding subscribers to the database
    """
    data = request.get_json()
    email = data.get('email')
    if (not email):
        return jsonify(result={'failed_msg': "Unable to save subscriber with missing email field, please add an email and try again"})

    return jsonify(result=save_subscriber(email))


@subscriber_bp.route('', methods=['GET'])
def get_subscriber_data():
    """ This function is used to get all the subscribers from the database """
    return jsonify(result=get_subscribers())


@subscriber_bp.route('', methods=['DELETE'])
def delete_subscriber_data():
    """ This function is used to delete a particular news item """
    data = request.args
    subscriber_id = data.get('id')
    results, status_code = delete_subscriber(subscriber_id)
    return jsonify(result=results), status_code

from flask import Blueprint, request, jsonify


carousel_bp = Blueprint('carousel', __name__, url_prefix='/api/carousel/')

from .utils import save_carousel, get_carousels, delete_carousel


@carousel_bp.route('', methods=["POST"])
def add_carousels():
    """ This function is used to get the request for adding Carousels to the database
    """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    rank = data.get('rank')
    title = data.get('title')

    if (not image) or (not description) or (not rank) or (not title):
        return jsonify(result={'failed_msg': "Unanle to save carousel with missing fields"})

    return jsonify(result=save_carousel(image, description, rank, title))


@carousel_bp.route('', methods=['PUT'])
def update_carousels():
    """ This function is used to update any existing carousel """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    rank = data.get('rank')
    title = data.get('title')
    carousel_id = data.get('id')

    if (not image) or (not description) or (not rank) or (not carousel_id) or (not title):
        return jsonify(result={'failed_msg': "Unable to update carousel with missing fields"})

    return jsonify(result=save_carousel(image, description, rank, title, _id=carousel_id))


@carousel_bp.route('', methods=['GET'])
def get_carousel_data():
    """ This function is used to get all the carousels from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_carousels(maximum=maxim))


@carousel_bp.route('', methods=['DELETE'])
def delete_carousel_data():
    """ This function is used to delete a particular news item """
    data = request.args
    carousel_id = data.get('id')
    results, status_code = delete_carousel(carousel_id)
    return jsonify(result=results), status_code

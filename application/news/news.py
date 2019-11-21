from flask import Blueprint, request, jsonify


news_bp = Blueprint('news', __name__, url_prefix='/api/news/')

from .utils import save_news, get_newses

@news_bp.route('', methods=["POST"])
def add_news():
    """ This function is used to get the request for adding Carousels to the database
    """
    data = request.args
    description = data.get('description')
    image = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save carousel with missing fields"})

    return jsonify(result=save_news(title, description, rank))


@carousel_bp.route('', methods=['PUT'])
def update_carousels():
    """ This function is used to update any existing carousel """
    data = request.args
    description = data.get('description')
    image = data.get('image')
    rank = data.get('rank')
    carousel_id = data.get('id')

    if (not image) or (not description) or (not rank) or (not carousel_id):
        return jsonify(result={'failed_msg': "Unable to update carousel with missing fields"})

    return jsonify(result=save_carousel(image, description, rank, _id=carousel_id))


@carousel_bp.route('', methods=['GET'])
def get_carousel_data():
    """ This function is used to get all the carousels from the database """
    return jsonify(result=get_carousels())
    

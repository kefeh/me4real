from flask import Blueprint, request, jsonify


news_bp = Blueprint('news', __name__, url_prefix='/api/news/')

from .utils import save_news, get_newses

@news_bp.route('', methods=["POST"])
def add_news():
    """ This function is used to get the request for adding news to the database
    """
    data = request.args
    description = data.get('description')
    image = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save news with missing fields"})

    return jsonify(result=save_news(title, description, rank))


@news_bp.route('', methods=["POST"])
def update_news():
    """ This function is used to get the request for adding news to the database
    """
    data = request.args
    description = data.get('description')
    image = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save news with missing fields"})

    return jsonify(result=save_news(title, description, rank))


@carousel_bp.route('', methods=['GET'])
def get_carousel_data():
    """ This function is used to get all the carousels from the database """
    return jsonify(result=get_carousels())
    

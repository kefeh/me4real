from flask import Blueprint, request, jsonify


news_bp = Blueprint('news', __name__, url_prefix='/api/news/')

from .utils import save_news, get_news, delete_news

@news_bp.route('', methods=["POST"])
def add_news():
    """ This function is used to get the request for adding news to the database
    """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save news with missing fields"})

    return jsonify(result=save_news(title, description, rank, image))


@news_bp.route('', methods=["PUT"])
def update_news():
    """ This function is used to get the request for adding news to the database
    """
    data = request.get_json()
    description = data.get('description')
    title = data.get('title')
    image = data.get('image')
    rank = data.get('rank')
    news_id = data.get('id')

    if (not title) or (not description) or (not rank) or (not news_id):
        return jsonify(result={'failed_msg': "Unanle to save news with missing fields"})

    return jsonify(result=save_news(title, description, rank, image, _id=news_id))


@news_bp.route('', methods=['GET'])
def get_news_data():
    """ This function is used to gets all number of specified news items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_news(maximum=maxim))


@news_bp.route('', methods=['DELETE'])
def delete_news_data():
    """ This function is used to delete a particular news item """
    data = request.args
    news_id = data.get('id')
    results, status_code = delete_news(news_id)
    return jsonify(result=results), status_code
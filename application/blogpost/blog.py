from flask import Blueprint, request, jsonify


blog_bp = Blueprint('blog', __name__, url_prefix='/api/blogs/')

from .utils import save_blog, get_blog, delete_blog

@blog_bp.route('', methods=["POST"])
def add_blog():
    """ This function is used to get the request for adding blog to the database
    """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save blog with missing fields"})

    return jsonify(result=save_blog(title, description, rank, image))


@blog_bp.route('', methods=["PUT"])
def update_blog():
    """ This function is used to get the request for adding blog to the database
    """
    data = request.get_json()
    description = data.get('description')
    title = data.get('title')
    image = data.get('image')
    rank = data.get('rank')
    blog_id = data.get('id')

    if (not title) or (not description) or (not rank) or (not blog_id):
        return jsonify(result={'failed_msg': "Unanle to save blog with missing fields"})

    return jsonify(result=save_blog(title, description, rank, image, _id=blog_id))


@blog_bp.route('', methods=['GET'])
def get_blog_data():
    """ This function is used to gets all number of specified blog items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_blog(maximum=maxim))


@blog_bp.route('', methods=['DELETE'])
def delete_blog_data():
    """ This function is used to delete a particular blog item """
    data = request.args
    blog_id = data.get('id')
    results, status_code = delete_blog(blog_id)
    return jsonify(result=results), status_code
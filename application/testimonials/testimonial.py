from flask import Blueprint, request, jsonify


testimonial_bp = Blueprint('testimonial', __name__, url_prefix='/api/testimonials/')

from .utils import save_testimonial, get_testimonial, delete_testimonial

@testimonial_bp.route('', methods=["POST"])
def add_testimonial():
    """ This function is used to get the request for adding testimonial to the database
    """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save testimonial with missing fields"})

    return jsonify(result=save_testimonial(title, description, rank, image))


@testimonial_bp.route('', methods=["PUT"])
def update_testimonial():
    """ This function is used to get the request for adding testimonial to the database
    """
    data = request.get_json()
    description = data.get('description')
    title = data.get('title')
    image = data.get('image')
    rank = data.get('rank')
    testimonial_id = data.get('id')

    if (not title) or (not description) or (not rank) or (not testimonial_id):
        return jsonify(result={'failed_msg': "Unanle to save testimonial with missing fields"})

    return jsonify(result=save_testimonial(title, description, rank, image, _id=testimonial_id))


@testimonial_bp.route('', methods=['GET'])
def get_testimonial_data():
    """ This function is used to gets all number of specified testimonial items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_testimonial(maximum=maxim))


@testimonial_bp.route('', methods=['DELETE'])
def delete_testimonial_data():
    """ This function is used to delete a particular testimonial item """
    data = request.args
    testimonial_id = data.get('id')
    results, status_code = delete_testimonial(testimonial_id)
    return jsonify(result=results), status_code
from flask import Blueprint, request, jsonify


programs_bp = Blueprint('programs', __name__, url_prefix='/api/programs/')

from .utils import save_programs, get_programs, delete_programs

@programs_bp.route('', methods=["POST"])
def add_programs():
    """ This function is used to get the request for adding programs to the database
    """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save programs with missing fields"})

    return jsonify(result=save_programs(title, description, rank, image))


@programs_bp.route('', methods=["PUT"])
def update_programs():
    """ This function is used to get the request for adding programs to the database
    """
    data = request.get_json()
    description = data.get('description')
    title = data.get('title')
    image = data.get('image')
    rank = data.get('rank')
    programs_id = data.get('id')

    if (not title) or (not description) or (not rank) or (not programs_id):
        return jsonify(result={'failed_msg': "Unanle to save programs with missing fields"})

    return jsonify(result=save_programs(title, description, rank, image, _id=programs_id))


@programs_bp.route('', methods=['GET'])
def get_programs_data():
    """ This function is used to gets all number of specified programs items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_programs(maximum=maxim))


@programs_bp.route('', methods=['DELETE'])
def delete_programs_data():
    """ This function is used to delete a particular programs item """
    data = request.args
    programs_id = data.get('id')
    results, status_code = delete_programs(programs_id)
    return jsonify(result=results), status_code
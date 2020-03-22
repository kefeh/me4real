from flask import Blueprint, request, jsonify


projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects/')

from .utils import save_projects, get_projects, delete_projects

@projects_bp.route('', methods=["POST"])
def add_projects():
    """ This function is used to get the request for adding projects to the database
    """
    data = request.get_json()
    description = data.get('description')
    image = data.get('image')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save projects with missing fields"})

    return jsonify(result=save_projects(title, description, rank, image))


@projects_bp.route('', methods=["PUT"])
def update_projects():
    """ This function is used to get the request for adding projects to the database
    """
    data = request.get_json()
    description = data.get('description')
    title = data.get('title')
    image = data.get('image')
    rank = data.get('rank')
    projects_id = data.get('id')

    if (not title) or (not description) or (not rank) or (not projects_id):
        return jsonify(result={'failed_msg': "Unanle to save projects with missing fields"})

    return jsonify(result=save_projects(title, description, rank, image, _id=projects_id))


@projects_bp.route('', methods=['GET'])
def get_projects_data():
    """ This function is used to gets all number of specified projects items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_projects(maximum=maxim))


@projects_bp.route('', methods=['DELETE'])
def delete_projects_data():
    """ This function is used to delete a particular projects item """
    data = request.args
    projects_id = data.get('id')
    results, status_code = delete_projects(projects_id)
    return jsonify(result=results), status_code
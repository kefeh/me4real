from flask import Blueprint, request, jsonify


teams_bp = Blueprint('teams', __name__, url_prefix='/api/teams/')

from .utils import save_teams, get_teams, delete_teams

@teams_bp.route('', methods=["POST"])
def add_teams():
    """ This function is used to get the request for adding teams to the database
    """
    data = request.get_json()
    description = data.get('description', '')
    image = data.get('image')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not image) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save teams with missing fields"})

    return jsonify(result=save_teams(title, description, rank, image))


@teams_bp.route('', methods=["PUT"])
def update_teams():
    """ This function is used to get the request for adding teams to the database
    """
    data = request.get_json()
    description = data.get('description', '')
    title = data.get('title')
    image = data.get('image')
    rank = data.get('rank')
    team_id = data.get('id')

    if (not title) or (not image) or (not rank) or (not team_id):
        return jsonify(result={'failed_msg': "Unanle to save teams with missing fields"})

    return jsonify(result=save_teams(title, description, rank, image, _id=team_id))


@teams_bp.route('', methods=['GET'])
def get_teams_data():
    """ This function is used to gets all number of specified teams items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_teams(maximum=maxim))


@teams_bp.route('<string:team_mate_id>', methods=['DELETE'])
def delete_teams_data(team_mate_id):
    """ This function is used to delete a particular teams item """
    results, status_code = delete_teams(team_mate_id)
    return jsonify(result=results), status_code
from flask import Blueprint, request, jsonify


video_bp = Blueprint('video', __name__, url_prefix='/api/video/')

from .utils import  save_video, get_video, delete_video # video_decode_save,

# @video_bp.route('', methods=["POST"])
# def add_video():
#     """ This function is used to get the request for adding video to the database
#     """
#     data = request.get_json()
#     description = data.get('description', '')
#     image = data.get('video')
#     title = data.get('title')

#     if (not title) or (not video) or (not rank):
#         return jsonify(result={'error': "Unanle to save video with missing fields"}), 400

#     resp = video_decode_save(video, title, description)
#     if 'error' in response:
#         status_code = 400
#     else: 
#         status_code = 200

#     return jsonify(result=resp), status_code
@video_bp.route('', methods=["POST"])
def add_video():
    """ This function is used to get the request for adding video to the database
    """
    data = request.get_json()
    link = data.get('link')
    title = data.get('title')
    rank = data.get('rank')

    if (not title) or (not link) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save video with missing fields"})

    return jsonify(result=save_video(title, link, rank))


@video_bp.route('', methods=["PUT"])
def update_video():
    """ This function is used to get the request for adding video to the database
    """
    data = request.get_json()
    delink = data.get('link')
    title = data.get('title')
    rank = data.get('rank')
    video_id = data.get('id')

    if (not title) or (not link) or (not rank) or (not video_id):
        return jsonify(result={'failed_msg': "Unable to save video with missing fields"})

    return jsonify(result=save_video(title, link, rank, _id=video_id))


@video_bp.route('', methods=['GET'])
def get_video_data():
    """ This function is used to gets all number of specified video items from the database """
    data = request.args
    maxim = data.get('max')
    return jsonify(result=get_video(maximum=maxim))


@video_bp.route('', methods=['DELETE'])
def delete_video_data():
    """ This function is used to delete a particular video item """
    data = request.args
    video_id = data.get('id')
    results, status_code = delete_video(video_id)
    return jsonify(result=results), status_code
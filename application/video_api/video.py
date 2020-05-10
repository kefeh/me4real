from flask import Blueprint, request, jsonify


video_bp = Blueprint('video', __name__, url_prefix='/api/video/')

from .utils import video_decode_save

@video_bp.route('', methods=["POST"])
def add_video():
    """ This function is used to get the request for adding video to the database
    """
    data = request.get_json()
    description = data.get('description', '')
    image = data.get('video')
    title = data.get('title')

    if (not title) or (not video) or (not rank):
        return jsonify(result={'error': "Unanle to save video with missing fields"}), 400

    resp = video_decode_save(video, title, description)
    if 'error' in response:
        status_code = 400
    else: 
        status_code = 200

    return jsonify(result=resp), status_code

from flask import Blueprint, request, jsonify


image_bp = Blueprint('images', __name__, url_prefix='/api/images/')

from .utils import save_image, get_images, delete_image

@image_bp.route('', methods=["POST"])
def add_images():
    """ This function is used to get the request for adding Carousels to the database
    """
    data = request.get_json()
    image = data.get('image')
    name = data.get('name')

    if (not image):
        return jsonify(result={'failed_msg': "Unanle to save image with missing fields"})

    if (not name):
        from datetime import datetime
        ts = int(datetime.now().timestamp())
        name = 'me4real' + str(ts)

    resp = save_image(image, name)
    if 'error' in response:
        status_code = 400
    else:
        status_code = 200
    return jsonify(result= resp), status_code


@image_bp.route('', methods=["GET"])
def get_all_images():
    """ This function gets all the images that were added using the above post request"""
    return jsonify(result=get_images())


@image_bp.route('', methods=['DELETE'])
def delete_an_image():
    data = request.args
    image_url = data.get('image_name')

    value = delete_image(image_url)

    result = {}
    if value:
        resp = {'pass_msg': 'Delete Successful'}
        status_code = 204
    else:
        resp = {'fail_msg': 'Unable to delete image'}
        status_code = 404

    return jsonify(result=resp), status_code
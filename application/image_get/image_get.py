from flask import Blueprint, request, jsonify


image_bp = Blueprint('image', __name__, url_prefix='/api/image/')

from .utils import save_image, get_images, delete_image

@image_bp.route('', methods=["POST"])
def add_images():
    """ This function is used to get the request for adding Carousels to the database
    """
    data = request.get_json()
    image = data.get('image')
    name = data.get('name')

    if (not image) or (not name):
        return jsonify(result={'failed_msg': "Unanle to save carousel with missing fields"})

    return jsonify(result=save_image(image, name))


@image_bp.route('', methods=["GET"])
def get_images():
    """ This function gets all the images that were added using the above post request"""
    return jsonify(result=get_images())
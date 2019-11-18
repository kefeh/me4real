from flask import Blueprint, request, jsonify
from utils import *

carousel_bp = Blueprint('carousel', __name__)

@carousel_bp.route('', methods=["POST"])
def add_carousels():
    """ This function is used to get the request for adding Carousels to the database
    """
    data = request.args
    description = data.get('description')
    image = data.get('image')
    rank = data.get('rank')

    if (not image) or (not description) or (not rank):
        return jsonify(result={'failed_msg': "Unanle to save carousel with missing fields"})

    

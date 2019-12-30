from flask import Blueprint, request, jsonify


contact_bp = Blueprint('contact', __name__, url_prefix='/api/contact/')

from .utils import save_contact, get_contacts, delete_contact


@contact_bp.route('', methods=["POST"])
def add_contacts():
    """ This function is used to get the request for adding contacts to the database
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if (not name) or (not message) or (not email) or (not subject):
        return jsonify(result={'failed_msg': "Unanle to save contact with missing fields"})

    return jsonify(result=save_contact(name, message, email, subject))


@contact_bp.route('', methods=['PUT'])
def update_contacts():
    """ This function is used to update any existing contact """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    contact_id = data.get('id')

    if (not name) or (not message) or (not email) or (not subject) or (not contact_id):
        return jsonify(result={'failed_msg': "Unable to update contact with missing fields"})

    return jsonify(result=save_contact(name, message, email, subject, _id=contact_id))


@contact_bp.route('', methods=['GET'])
def get_contact_data():
    """ This function is used to get all the contacts from the database """
    data = request.args
    return jsonify(result=get_contacts())


@contact_bp.route('', methods=['DELETE'])
def delete_contact_data():
    """ This function is used to delete a particular news item """
    data = request.args
    contact_id = data.get('id')
    results, status_code = delete_contact(contact_id)
    return jsonify(result=results), status_code

from bson import ObjectId
from application.utils.utils import image_decode_save, delete_image_from_bucket, BASE_URl


def save_contact(image, description, rank, title, _id=None, count=0):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    a_contact = db.Contact() if not _id else db.Contact.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    if BASE_URl in image:
        pass
    else:
        image = image_decode_save(image, image_name, 'contact')
        if 'error' in image:
            return {'failed_msg': 'Could not upload image to the sever'}
        else:
            image = image.get('url')
    if value:
        a_contact['description'] = description
        a_contact['image'] = image
        a_contact['rank'] = rank
        a_contact['title'] = title
        try:
            a_contact.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save contact, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save contact, contact admin"}

    return get_contacts(cond=dict(a_contact))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_contact = db.Contact.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Contact.find_one({'rank': rank})
        if not some_contact:
            return True
        rank += 1
        some_contact['rank'] = rank
        try:
            some_contact.save()
            aldy_handled = some_contact.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def get_contacts(maximum=None, cond={}):
    from models import db
    if maximum:
        contacts = list(db.Contact.find({}).sort({'rank': 1}).limit(maximum)) if not cond else list(db.Contact.find(cond).sort({'rank': 1}).limit(maximum))
    else:
        contacts = list(db.Contact.find({})) if not cond else list(db.Contact.find(cond))
    for contact in contacts:
        contact['_id'] = str(contact['_id'])
    return contacts if (maximum or not cond) else contacts[0]


def delete_contact(contact_id):
    from models import db
    try:
        a_contact = db.Contact.find_one({'_id': ObjectId(contact_id)})
        image_url = a_contact.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.Contact.collection.remove({'_id': ObjectId(contact_id)})
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the news item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
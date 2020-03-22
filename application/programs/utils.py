from bson import ObjectId
from application.utils.utils import image_decode_save, BASE_URl


def save_programs(title, description, rank, image, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    programs_item = db.Program() if not _id else db.Program.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    if BASE_URl in image:
        pass
    else:
        image = image_decode_save(image, image_name, 'programs')
        if 'error' in image:
            return {'failed_msg': 'Could not upload image to the sever'}
        else:
            image = image.get('url')
    if value:
        programs_item['description'] = description
        programs_item['title'] = title
        programs_item['image'] = image
        programs_item['rank'] = rank
        try:
            programs_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_programs(cond=dict(programs_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_programs = db.Program.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Program.find_one({'rank': rank})
        if not some_programs:
            return True
        rank += 1
        some_programs['rank'] = rank
        try:
            some_programs.save()
            aldy_handled = some_programs.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def get_programs(maximum=None, cond={}):
    from models import db
    if maximum:
        programs = list(db.Program.find({}).sort({'rank': 1}).limit(maximum)) if not cond else list(db.Program.find(cond).sort({'rank': 1}).limit(maximum))
    else:
        programs = list(db.Program.find({})) if not cond else list(db.Program.find(cond))
    for an_item in programs:
        an_item['_id'] = str(an_item['_id'])
    return programs if (maximum or not cond) else programs[0]


def delete_programs(programs_id):
    from models import db
    try:
        a_programs = db.Program.find_one({'_id': ObjectId(programs_id)})
        image_url = a_programs.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.Program.collection.remove({'_id': ObjectId(programs_id)})
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the programs item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
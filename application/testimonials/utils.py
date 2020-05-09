from bson import ObjectId
from application.utils.utils import image_decode_save, BASE_URl


def save_testimonial(title, description, rank, image, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    testimonial_item = db.Testimonial() if not _id else db.Testimonial.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    if BASE_URl in image:
        pass
    else:
        image = image_decode_save(image, image_name, 'testimonial')
        if 'error' in image:
            return {'failed_msg': 'Could not upload image to the sever'}
        else:
            image = image.get('url')
    if value:
        testimonial_item['description'] = description
        testimonial_item['title'] = title
        testimonial_item['image'] = image
        testimonial_item['rank'] = rank
        try:
            testimonial_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_testimonial(cond=dict(testimonial_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_testimonial = db.Testimonial.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Testimonial.find_one({'rank': rank})
        if not some_testimonial:
            return True
        rank += 1
        some_testimonial['rank'] = rank
        try:
            some_testimonial.save()
            aldy_handled = some_testimonial.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def update_rank_reverse(rank):

    from models import db
    rank = int(rank)
    while rank:
        fwd_rank = rank + 1
        some_testimonial = db.Testimonial.find_one({'rank': fwd_rank})
        if not some_testimonial:
            return True
        some_testimonial['rank'] = rank
        try:
            some_testimonial.save()
            rank += 1
        except Exception as exp:
            return False
    
    return True


def get_testimonial(maximum=None, cond={}):
    from models import db
    if maximum:
        testimonial = list(db.Testimonial.find({}).sort([('rank', 1)]).limit(int(maximum))) if not cond else list(db.Testimonial.find(cond).sort([('rank', 1)]).limit(int(maximum)))
    else:
        testimonial = list(db.Testimonial.find({})) if not cond else list(db.Testimonial.find(cond))
    for an_item in testimonial:
        an_item['_id'] = str(an_item['_id'])
    return testimonial if (maximum or not cond) else testimonial[0]


def delete_testimonial(testimonial_id):
    from models import db
    try:
        a_testimonial = db.Testimonial.find_one({'_id': ObjectId(testimonial_id)})
        image_url = a_testimonial.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.Testimonial.collection.remove({'_id': ObjectId(testimonial_id)})
        update_rank_reverse(a_testimonial['rank'])
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the testimonial item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
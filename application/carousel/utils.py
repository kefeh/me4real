from bson import ObjectId
from application.utils.utils import image_decode_save, delete_image_from_bucket, BASE_URl


def save_carousel(image, description, rank, title, _id=None, count=0):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    a_carousel = db.Carousel() if not _id else db.Carousel.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    if BASE_URl in image:
        pass
    else:
        image = image_decode_save(image, image_name, 'carousel')
        if 'error' in image:
            return {'failed_msg': 'Could not upload image to the sever'}
        else:
            image = image.get('url')
    if value:
        a_carousel['description'] = description
        a_carousel['image'] = image
        a_carousel['rank'] = rank
        a_carousel['title'] = title
        try:
            a_carousel.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_carousels(cond=dict(a_carousel))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_carousel = db.Carousel.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Carousel.find_one({'rank': rank})
        if not some_carousel:
            return True
        rank += 1
        some_carousel['rank'] = rank
        try:
            some_carousel.save()
            aldy_handled = some_carousel.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def update_rank_reverse(rank):

    from models import db
    rank = int(rank)
    while rank:
        fwd_rank = rank + 1
        some_carousel = db.Carousel.find_one({'rank': fwd_rank})
        if not some_carousel:
            return True
        some_carousel['rank'] = rank
        try:
            some_carousel.save()
            rank += 1
        except Exception as exp:
            return False
    
    return True


def get_carousels(maximum=None, cond={}):
    from models import db
    if maximum:
        carousels = list(db.Carousel.find({}).sort([('rank', 1)]).limit(int(maximum))) if not cond else list(db.Carousel.find(cond).sort([('rank', 1)]).limit(int(maximum)))
    else:
        carousels = list(db.Carousel.find({})) if not cond else list(db.Carousel.find(cond))
    for carousel in carousels:
        carousel['_id'] = str(carousel['_id'])
    return carousels if (maximum or not cond) else carousels[0]


def delete_carousel(carousel_id):
    from models import db
    try:
        a_carousel = db.Carousel.find_one({'_id': ObjectId(carousel_id)})
        image_url = a_carousel.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.Carousel.collection.remove({'_id': ObjectId(carousel_id)})
        update_rank_reverse(a_carousel['rank'])
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the news item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
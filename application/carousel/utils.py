from bson import ObjectId


def save_carousel(image, description, rank, _id=None, count=0):
    from models import db
    rank = int(rank)
    value = update_ranks(rank)

    a_carousel = db.Carousel() if not _id else db.Carousel.find_one({'_id': ObjectId(_id)})
    if value:
        a_carousel['description'] = description
        a_carousel['image'] = image
        a_carousel['rank'] = rank
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
    value = True
    while rank:
        some_carousel = db.Carousel.find_one({'rank': rank})
        if not some_carousel:
            value = False
            break
        rank += 1
        some_carousel['rank'] = rank
        try:
            some_carousel.save()
        except Exception as exp:
            raise
            value = False
            break

    return True


def get_carousels(maximum=None, cond={}):
    from models import db
    if maximum:
        cond = {'rank': {'$lte': int(maximum)}}
    carousels = list(db.Carousel.find({})) if not cond else list(db.Carousel.find(cond))
    for carousel in carousels:
        carousel['_id'] = str(carousel['_id'])
    return carousels if (maximum or not cond) else carousels[0]
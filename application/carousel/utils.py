from models import db
from bson import ObjectId

def save_carousel(image, description, rank, _id=None):
    a_carousel = db.Carousel() if not _id else db.Carousel.find_one({'_id': ObjectId(_id)})
    some_carousel = db.Carousel.find_one({'rank': rank})
    rank = int(rank)
    a_carousel['description'] = description
    a_carousel['image'] = image
    a_carousel['rank'] = rank
    try:
        a_carousel.save()
    except Exception as exp:
        print(exp)
        return {}
    if some_carousel:
        save_carousel(some_carousel['image'], some_carousel['description'], some_carousel['rank'] + 1, some_carousel['_id'])

    return get_carousels()

def get_carousels():
    carousels = list(db.Carousel.find({}))
    for carousel in carousels:
        carousel['_id'] = str(carousel['_id'])
    return carousels
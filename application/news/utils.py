from bson import ObjectId
from application.utils.utils import image_decode_save


def save_news(title, description, rank, image, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    news_item = db.News() if not _id else db.News.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    image = image_decode_save(image, image_name, 'news')
    if 'error' in image:
        return {'failed_msg': 'Could not upload image to the sever'}
    else:
        image = image.get('url')
    if value:
        news_item['description'] = description
        news_item['title'] = title
        news_item['image'] = image
        news_item['rank'] = rank
        try:
            news_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_news(cond=dict(news_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_news = db.News.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.News.find_one({'rank': rank})
        if not some_news:
            return True
        rank += 1
        some_news['rank'] = rank
        try:
            some_news.save()
            aldy_handled = some_news.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def get_news(maximum=None, cond={}):
    from models import db
    if maximum:
        cond['rank'] = {'$lte': int(maximum)}
    news = list(db.News.find({})) if not cond else list(db.News.find(cond))
    for an_item in news:
        an_item['_id'] = str(an_item['_id'])
    return news if (maximum or not cond) else news[0]


def delete_news(news_id):
    from models import db
    try:
        a_news = db.News.find_one({'_id': ObjectId(news_id)})
        image_url = a_news.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.News.collection.remove({'_id': ObjectId(news_id)})
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the news item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
from bson import ObjectId


def save_news(title, description, rank, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    news_item = db.News() if not _id else db.News.find_one({'_id': ObjectId(_id)})
    if value:
        news_item['description'] = description
        news_item['title'] = title
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
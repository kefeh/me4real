from models import db
from bson import ObjectId

def save_news(title, description, rank, _id=None):
    rank = int(rank)
    news_item = db.News() if not _id else db.Carousel.find_one({'_id': ObjectId(_id)})
    some_news = db.News.find_one({'rank': rank})
    news_item['description'] = description
    news_item['title'] = title
    news_item['rank'] = rank
    try:
        news_item.save()
    except Exception as exp:
        print(exp)
        return {}
    if some_news:
        save_news(some_news['title'], some_news['description'], some_news['rank'] + 1, some_news['_id'])

    return get_news()

def get_news():
    news = list(db.News.find({}))
    for a_news in news:
        a_news['_id'] = str(a_news['_id'])
    return news
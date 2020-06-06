from bson import ObjectId


def save_events(title, description, rank, time, location, latitude, longitude, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    events_item = db.Event() if not _id else db.Event.find_one({'_id': ObjectId(_id)})

    if value:
        events_item['description'] = description
        events_item['title'] = title
        events_item['time'] = time
        events_item['location'] = location
        events_item['latitude'] = latitude
        events_item['longitude'] = longitude
        events_item['rank'] = rank
        try:
            events_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_events(cond=dict(events_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_events = db.Event.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Event.find_one({'rank': rank})
        if not some_events:
            return True
        rank += 1
        some_events['rank'] = rank
        try:
            some_events.save()
            aldy_handled = some_events.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def update_rank_reverse(rank):

    from models import db
    rank = int(rank)
    while rank:
        fwd_rank = rank + 1
        some_events = db.Event.find_one({'rank': fwd_rank})
        if not some_events:
            return True
        some_events['rank'] = rank
        try:
            some_events.save()
            rank += 1
        except Exception as exp:
            return False
    
    return True


def get_events(maximum=None, cond={}):
    from models import db
    if maximum:
        events = list(db.Event.find({}).sort([('rank', 1)]).limit(int(maximum))) if not cond else list(db.Event.find(cond).sort([('rank', 1)]).limit(int(maximum)))
    else:
        events = list(db.Event.find({})) if not cond else list(db.Event.find(cond))
    for an_item in events:
        an_item['_id'] = str(an_item['_id'])
    return events if (maximum or not cond) else events[0]


def delete_events(events_id):
    from models import db
    try:
        a_events = db.Event.find_one({'_id': ObjectId(events_id)})
        db.Event.collection.remove({'_id': ObjectId(events_id)})
        update_rank_reverse(a_events['rank'])
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the events item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
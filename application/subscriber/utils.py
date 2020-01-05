from bson import ObjectId


def save_subscriber(email):

    from models import db
    
    subscriber = db.Subscriber()
    if email:
        subscriber['email'] = email
        try:
            subscriber.save()
        except Exception as exp:
            print(exp)
            return {'error': "Database issues, unable to save Subscriber email"}
    else:
        return {'error': "Database issues, unable to save Subscriber email"}

    return {'pass_msg': f"Successfully suscribed {email} for me4real monthly updates"}


def get_subscribers(cond={}):

    from models import db
    
    subscribers = list(db.Subscriber.find({})) if not cond else list(db.Subscriber.find(cond))
    for subscriber in subscribers:
        subscriber['_id'] = str(subscriber['_id'])
    return subscribers


def delete_subscriber(subscriber_id):
    from models import db
    try:
        db.Subscriber.collection.remove({'_id': ObjectId(subscriber_id)})
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the Subscriber email with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
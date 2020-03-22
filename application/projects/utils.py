from bson import ObjectId
from application.utils.utils import image_decode_save, BASE_URl


def save_projects(title, description, rank, image, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    projects_item = db.Project() if not _id else db.Project.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    if BASE_URl in image:
        pass
    else:
        image = image_decode_save(image, image_name, 'projects')
        if 'error' in image:
            return {'failed_msg': 'Could not upload image to the sever'}
        else:
            image = image.get('url')
    if value:
        projects_item['description'] = description
        projects_item['title'] = title
        projects_item['image'] = image
        projects_item['rank'] = rank
        try:
            projects_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_projects(cond=dict(projects_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_projects = db.Project.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Project.find_one({'rank': rank})
        if not some_projects:
            return True
        rank += 1
        some_projects['rank'] = rank
        try:
            some_projects.save()
            aldy_handled = some_projects.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def get_projects(maximum=None, cond={}):
    from models import db
    if maximum:
        projects = list(db.Project.find({}).sort({'rank': 1}).limit(maximum)) if not cond else list(db.Project.find(cond).sort({'rank': 1}).limit(maximum))
    else:
        projects = list(db.Project.find({})) if not cond else list(db.Project.find(cond))
    for an_item in projects:
        an_item['_id'] = str(an_item['_id'])
    return projects if (maximum or not cond) else projects[0]


def delete_projects(projects_id):
    from models import db
    try:
        a_projects = db.Project.find_one({'_id': ObjectId(projects_id)})
        image_url = a_projects.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.Project.collection.remove({'_id': ObjectId(projects_id)})
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the projects item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
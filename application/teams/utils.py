from bson import ObjectId
from application.utils.utils import image_decode_save


def save_teams(title, description, rank, image, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    teams_item = db.Team() if not _id else db.Team.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    image = image_decode_save(image, image_name, 'teams')
    if 'error' in image:
        return {'failed_msg': 'Could not upload image to the sever'}
    else:
        image = image.get('url')
    if value:
        teams_item['description'] = description
        teams_item['title'] = title
        teams_item['image'] = image
        teams_item['rank'] = rank
        try:
            teams_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_teams(cond=dict(teams_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_teams = db.Team.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Team.find_one({'rank': rank})
        if not some_teams:
            return True
        rank += 1
        some_teams['rank'] = rank
        try:
            some_teams.save()
            aldy_handled = some_teams.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def get_teams(maximum=None, cond={}):
    from models import db
    if maximum:
        cond['rank'] = {'$lte': int(maximum)}
    teams = list(db.Team.find({})) if not cond else list(db.Team.find(cond))
    for an_item in teams:
        an_item['_id'] = str(an_item['_id'])
    return teams if (maximum or not cond) else teams[0]


def delete_teams(team_mate_id):
    from models import db
    try:
        a_team = db.Team.find_one({'_id': ObjectId(team_id)})
        image_url = a_team.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
    
        db.Team.collection.remove({'_id': ObjectId(team_mate_id)})
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the teams item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
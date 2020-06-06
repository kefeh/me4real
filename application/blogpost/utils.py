from bson import ObjectId
from application.utils.utils import image_decode_save, BASE_URl, delete_image_from_bucket


def save_blog(title, description, rank, image, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    blog_item = db.Blog() if not _id else db.Blog.find_one({'_id': ObjectId(_id)})
    image_name = str(title).replace(' ', '_')
    if BASE_URl in image:
        pass
    else:
        image = image_decode_save(image, image_name, 'blog')
        if 'error' in image:
            return {'failed_msg': 'Could not upload image to the sever'}
        else:
            image = image.get('url')
    if value:
        blog_item['description'] = description
        blog_item['title'] = title
        blog_item['image'] = image
        blog_item['rank'] = rank
        try:
            blog_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Carousel, contact admin"}

    return get_blog(cond=dict(blog_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_blog = db.Blog.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Blog.find_one({'rank': rank})
        if not some_blog:
            return True
        rank += 1
        some_blog['rank'] = rank
        try:
            some_blog.save()
            aldy_handled = some_blog.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def update_rank_reverse(rank):

    from models import db
    rank = int(rank)
    while rank:
        fwd_rank = rank + 1
        some_blog = db.Blog.find_one({'rank': fwd_rank})
        if not some_blog:
            return True
        some_blog['rank'] = rank
        try:
            some_blog.save()
            rank += 1
        except Exception as exp:
            return False
    
    return True


def get_blog(maximum=None, cond={}):
    from models import db
    if maximum:
        blog = list(db.Blog.find({}).sort([('rank', 1)]).limit(int(maximum))) if not cond else list(db.Blog.find(cond).sort([('rank', 1)]).limit(int(maximum)))
    else:
        blog = list(db.Blog.find({})) if not cond else list(db.Blog.find(cond))
    for an_item in blog:
        an_item['_id'] = str(an_item['_id'])
    return blog if (maximum or not cond) else blog[0]


def delete_blog(blog_id):
    from models import db
    try:
        a_blog = db.Blog.find_one({'_id': ObjectId(blog_id)})
        image_url = a_blog.get('image')
        image_key = image_url.split('/')[-1]

        delete_image_from_bucket(image_key)
        db.Blog.collection.remove({'_id': ObjectId(blog_id)})
        update_rank_reverse(a_blog['rank'])
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the blog item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204
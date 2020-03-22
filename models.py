from main import connection
from mongokit import Document


class User(Document):
    __collection__ = "user"
    structure = {
        'name': str,
        'email': str,
    }

    use_dot_notation = True
    def __repr__(self):
        return f'user is {self.name}'


class Carousel(Document):
    __collection__ = 'carousels'
    structure = {
        'description': str,
        'rank': int,
        'image': str, # the string here will be in base 64 so that should be noted
        'title': str,
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'image', 'title']


class News(Document):
    __collection__ = 'news'
    structure = {
        'title': str,
        'image': str,
        'description': str,
        'rank': int,
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'title']



class Program(Document):
    __collection__ = 'programs'
    structure = {
        'title': str,
        'image': str,
        'description': str,
        'rank': int,
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'title']


class Project(Document):
    __collection__ = 'projects'
    structure = {
        'title': str,
        'image': str,
        'description': str,
        'rank': int,
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'title']


class Event(Document):
    __collection__ = 'events'
    structure = {
        'title': str,
        'image': str,
        'description': str,
        'rank': int,
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'title']


class Team(Document):
    __collection__ = 'teams'
    structure = {
        'title': str,
        'description': str,
        'rank': int,
        'image': str,
    }

    use_dot_notation = True
    required_fields = ['image', 'rank', 'title']


class Subscriber(Document):
    __collection__ = 'subscribers'
    structure = {
        'email': str
    }

    use_dot_notation = True
    required_fields = ['email']


# Register the models
connection.register([User, Carousel, News, Team, Subscriber])

db = connection.me4real

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


class Blog(Document):
    __collection__ = 'blogs'
    structure = {
        'title': str,
        'image': str,
        'description': str,
        'rank': int,
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'title']


class Testimonial(Document):
    __collection__ = 'testimonials'
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
        'time': str,
        'description': str,
        'location': str,
        'latitude': str,
        'longitude': str,
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


class Video(Document):
    __collection__ = 'videos'
    structure = {
        'title': str,
        'link': str,
        'rank': int,
        'date': str,
    }

    use_dot_notation = True
    required_fields = ['title', 'link', 'rank', 'date']


# Register the models
connection.register([User, Carousel, News, Team, Subscriber, Event, Blog, Project, Program, Testimonial, Video])

db = connection.me4real

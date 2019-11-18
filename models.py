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
    }

    use_dot_notation = True
    required_fields = ['description', 'rank', 'image']


# Register the models
connection.register([User, Carousel])

db = connection.me4real

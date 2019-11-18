from app import db
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


# Register the models
db.register([User])

db = db.me4real

from app import app
from models import db

print(db.User.find_one())


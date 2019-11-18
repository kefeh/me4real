from flask import Flask
from mongokit import Connection

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

# connect to  the database
db = Connection(
    app.config['MONGODB_HOST'],
    app.config['MONGODB_PORT'],
)


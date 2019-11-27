from flask import Flask
from flask_cors import CORS
from mongokit import Connection
from middleware import Middleware


# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, origins='*')

# calling our middleware
app.wsgi_app = Middleware(app, app.wsgi_app)

# connect to  the database
connection = Connection(
    app.config['MONGODB_HOST'],
    app.config['MONGODB_PORT'],
)


# Blueprint Imports
from application.carousel.carousel import carousel_bp
from application.news.news import news_bp


# Registering my blueprints
app.register_blueprint(carousel_bp)
app.register_blueprint(news_bp)



if __name__ == '__main__':
    app.run(debug=True)

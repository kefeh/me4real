from main import app
from models import db

app.run()
print(db.User.find_one())


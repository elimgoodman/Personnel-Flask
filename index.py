import os
from config import get_config
from flask import Flask
import bcrypt
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_config('DATABASE_URL')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)

    def __init__(self, first_name, last_name, password, email):
        salt = get_config("PW_SALT")

        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = bcrypt.hashpw(password, salt)
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.first_name

db.create_all()

@app.route('/')
def hello():
    u = User("Eli", "Goodman", "password", "eli.m.goodman@gmail.com")
    db.session.add(u)
    db.session.commit()

    users = User.query.all()
    print users
    return 'Hi'

if __name__ == "__main__":
    app.run(debug=True)
from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from index import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)

    def __init__(self, first_name, last_name, password, email):
        salt = app.config.get("PW_SALT")

        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = bcrypt.hashpw(password, salt)
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.first_name

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.id

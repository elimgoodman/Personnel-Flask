from app.people.models import Person
from flask.ext.sqlalchemy import SQLAlchemy
from app import db, app
from sqlalchemy.orm import relationship, backref
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    person = relationship("Person", uselist=False, backref="user")

    def __init__(self, email, password):
        salt = app.config.get("PW_SALT")

        self.email = email
        self.password_hash = bcrypt.hashpw(password, salt)

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.id

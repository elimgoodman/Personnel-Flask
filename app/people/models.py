from flask.ext.sqlalchemy import SQLAlchemy
from app import db, app
import bcrypt

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    managed_by_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __init__(self, user_id, first_name, last_name, managed_by_id = None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.managed_by_id = managed_by_id

    def __repr__(self):
        return '<Person %r>' % self.first_name

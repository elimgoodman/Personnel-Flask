from flask.ext.sqlalchemy import SQLAlchemy
from app import db, app

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

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date = db.Column(db.Date)

    def __init__(self, author_id, subject_id, date):
        self.author_id = author_id
        self.subject_id = subject_id
        self.date = date

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    note_type = db.Column(db.String(16))
    body = db.Column(db.Text)
    linked_feedback = db.Column(db.Integer, db.ForeignKey('feedback.id'))
    linked_checkin = db.Column(db.Integer, db.ForeignKey('checkin.id'))
    
    def __init__(self, entry_id, note_type, body):
        self.entry_id = entry_id
        self.note_type = note_type
        self.body = body

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    has_communicated = db.Column(db.Date)
    date_communicated = db.Column(db.Date)
    body = db.Column(db.Text)

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    for_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date_to_check_in = db.Column(db.Date)
    has_checked_in = db.Column(db.Date)
    date_checked_in = db.Column(db.Date)
    body = db.Column(db.Text)

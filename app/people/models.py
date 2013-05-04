from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
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
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    note_type = db.Column(db.String(16))
    body = db.Column(db.Text)
    is_pinned = db.Column(db.Boolean)
    linked_feedback = db.Column(db.Integer, db.ForeignKey('feedback.id'))
    person = relationship("Entry", backref="notes")

    def __init__(self, entry, note_type, body, is_pinned=False, linked_feedback=None):
        self.entry_id = entry.id
        self.subject_id = entry.subject_id
        self.author_id = entry.author_id
        self.note_type = note_type
        self.body = body
        self.linked_feedback = linked_feedback
        self.is_pinned = is_pinned

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    has_communicated = db.Column(db.Boolean)
    body = db.Column(db.Text)
    note = relationship("Note", backref="feedback", uselist=False)
    from_person = relationship("Person", backref="feedback_given", foreign_keys=[from_id])
    to_person = relationship("Person", backref="feedback_taken", foreign_keys=[to_id])

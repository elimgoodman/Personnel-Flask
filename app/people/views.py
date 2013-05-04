import json, datetime
from app.util import common_render, to_json
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from app.users.models import User
from app.people.models import Person, Entry, Note, Feedback
from app import app, login_manager, db
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators

mod = Blueprint('people', __name__, url_prefix="/people", template_folder="templates")

@mod.route("/")
@login_required
def all():
    return common_render('all.jinja')

class PersonForm(Form):
    first_name = TextField('First Name', [validators.Required()])
    last_name = TextField('Last Name', [validators.Required()])

@mod.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = PersonForm(request.form)
    if request.method == 'POST' and form.validate():
        current_person_id = current_user.person.id

        p = Person(
            None,
            form.first_name.data,
            form.last_name.data,
            current_person_id
        )

        db.session.add(p)
        db.session.commit()
        flash("Person successfully added.")
        return redirect(url_for("people.all"))
    else:
        return common_render('add.jinja', form=form)

class UnauthorizedException(Exception): pass

def get_person(person_id):
    p = Person.query.filter(Person.id == person_id).one()

    if p.managed_by_id != current_user.person.id:
        raise UnauthorizedException

    return p

@mod.route("/<int:person_id>") 
@login_required
def view(person_id):
    try:
        p = get_person(person_id)
    except NoResultFound:
        return common_render("404.jinja"), 404
    except UnauthorizedException:
        return common_render("error.jinja"), 403

    entries = Entry.query.filter(Entry.subject_id == p.id).all()
    return common_render("view.jinja", person=p, entries=entries)

@mod.route("/<int:person_id>/entries/add", methods=["GET", "POST"]) 
@login_required
def add_entry(person_id):
    try:
        subject = get_person(person_id)
    except NoResultFound:
        return common_render("404.jinja"), 404
    except UnauthorizedException:
        return common_render("error.jinja"), 403

    #fetch and serlialize all people managed by the current user
    current_person_id = current_user.person.id

    managed_by = Person.query.filter(and_(\
            Person.managed_by_id == current_person_id,\
            Person.id != subject.id))\
            .all()

    managed_by = [to_json(p, Person) for p in managed_by]
    managed_by_str = json.dumps(managed_by)

    # get all pinned notes
    pinned = Note.query.filter(and_(\
            Note.is_pinned == True, \
            Note.author_id == current_person_id, \
            Note.subject_id == subject.id)).all()

    pinned = [to_json(p, Note) for p in pinned]
    pinned_str = json.dumps(pinned)

    # get all feedback
    feedback = Feedback.query.filter(and_(\
            Feedback.to_id == subject.id,
            Feedback.has_communicated == False)).all()

    feedback = [to_json(p, Feedback) for p in feedback]
    feedback_str = json.dumps(feedback)

    if request.method == 'POST':

        e = Entry(current_user.person.id, subject.id, datetime.date.today())
        db.session.add(e)
        db.session.commit()

        notes = json.loads(request.form['notes'])

        for note in notes:
            if note['body']:
                if note['type'] == "FEEDBACK":
                    f = Feedback()
                    f.from_id = subject.id
                    f.to_id = int(note['meta']['feedback-for'])
                    f.has_communicated = False
                    f.body = note['body']

                    #FIXME: this could lead to numerous commits
                    db.session.add(f)
                    db.session.commit()
                else:
                    f = None

                is_pinned = note['type'] == 'CHECKIN'
                n = Note(e, note["type"], note['body'], is_pinned=is_pinned)
            
                if f:
                    n.linked_feedback = f.id

                db.session.add(n)

        db.session.commit()
        return redirect(url_for("people.view", person_id=subject.id))

    return common_render("add_entry.jinja", \
            person=subject,\
            managed_by_str=managed_by_str,\
            feedback_str=feedback_str,\
            pinned_str=pinned_str)

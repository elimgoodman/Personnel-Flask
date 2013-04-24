from app.util import common_render
from sqlalchemy.orm.exc import NoResultFound
from app.users.models import User
from app.people.models import Person
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


@mod.route("/<int:id>") 
@login_required
def view(id):
    p = Person.query.filter(Person.id == id).one()
    return common_render("view.jinja", person=p)

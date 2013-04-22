import bcrypt
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from app.users.models import User
from app import app, login_manager, common_render, db
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators

mod = Blueprint('users', __name__, template_folder="templates")

@login_manager.user_loader
def load_user(userid):
    id = int(userid)
    try:
        return User.query.filter(User.id == id).one()
    except NoResultFound:
        return None

class RegistrationForm(Form):
    first_name = TextField('First Name')
    last_name = TextField('Last Name')
    email = TextField('Email Address')
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = TextField('Email Address', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

@mod.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = app.config.get("PW_SALT")
    
        user = User(
            form.email.data,
            form.password.data
        )

        db.session.add(user)
        db.session.commit()
        
        person = Person(
            user.id,
            form.first_name.data, 
            form.last_name.data
        )

        db.session.add(person)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))
    return common_render('register.jinja', form=form)

@mod.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = app.config.get("PW_SALT")
        password_hash = bcrypt.hashpw(form.password.data, salt)

        clause = and_(User.email == form.email.data, User.password_hash == password_hash)

        try:
            user = User.query.filter(clause).one()
        except NoResultFound:
            flash("Incorrect email address or password.")
            return common_render('login.jinja', form=form)

        login_user(user)
        return redirect(url_for('index'))
    return common_render('login.jinja', form=form)

@mod.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

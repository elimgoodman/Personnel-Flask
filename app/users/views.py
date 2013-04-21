from app import app
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"

mod = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(userid):
    id = int(userid)
    return User.query.filter(User.id == id).one()

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

def common_render(tmpl_name, **kwargs):
    common_args = {
        "user": current_user
    }

    kwargs.update(common_args)
    return render_template(tmpl_name, **kwargs)

@mod.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = get_config("PW_SALT")
    
        user = User(
            form.first_name.data, 
            form.last_name.data, 
            form.password.data,
            form.email.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))
    return common_render('register.jinja', form=form)

@mod.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = get_config("PW_SALT")
        password_hash = bcrypt.hashpw(form.password.data, salt)

        clause = and_(User.email == form.email.data, User.password_hash == password_hash)
        print form.email.data
        user = User.query.filter(clause).one()

        login_user(user)
        return redirect(url_for('index'))
    return common_render('login.jinja', form=form)

@mod.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

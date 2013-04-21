import os
from config import get_config
from flask import Flask, redirect, url_for, request, render_template
import bcrypt
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_config('DATABASE_URL')
app.secret_key = get_config("TOKEN_SECRET")
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"

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

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.id

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

@app.route("/register", methods=["GET", "POST"])
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

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/')
def index():
    if current_user.is_anonymous():
        return common_render('splash.jinja')
    else:
        return common_render('dashboard.jinja')

if __name__ == "__main__":
    app.run(debug=True)
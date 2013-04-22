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


if __name__ == "__main__":
    app.run(debug=True)
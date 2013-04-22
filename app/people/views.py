import bcrypt
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from app.users.models import User
from app import app, login_manager, common_render, db
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators

mod = Blueprint('people', __name__, url_prefix="/people", template_folder="templates")

@mod.route("/")
@login_required
def all():
    print current_user.person.user
    return common_render('all.jinja')

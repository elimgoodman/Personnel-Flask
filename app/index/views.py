from app.util import common_render
from flask_login import current_user
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

mod = Blueprint('index', __name__, template_folder="templates")

@mod.route('/')
def index():
    if current_user.is_anonymous():
        return common_render('splash.jinja')
    else:
        return common_render('dashboard.jinja')

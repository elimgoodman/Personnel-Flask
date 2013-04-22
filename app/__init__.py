from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app_config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.jinja'), 404

@app.route('/')
def index():
    if current_user.is_anonymous:
        return common_render('splash.jinja')
    else:
        return common_render('dashboard.jinja')

from app.users.views import mod as usersModule
app.register_blueprint(usersModule)


from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('app_config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "users.login"

#FIXME: prob not the best place for this
def common_render(tmpl_name, **kwargs):
    common_args = {
        "user": current_user,
        "config": app.config
    }

    kwargs.update(common_args)
    return render_template(tmpl_name, **kwargs)

@app.errorhandler(404)
def not_found(error):
    return common_render('404.jinja'), 404

@app.route('/')
def index():
    if current_user.is_anonymous():
        return common_render('splash.jinja')
    else:
        return common_render('dashboard.jinja')

from app.users.views import mod as usersModule
app.register_blueprint(usersModule)

from app.people.views import mod as peopleModule
app.register_blueprint(peopleModule)

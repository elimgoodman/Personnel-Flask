from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

print "a"

app = Flask(__name__)
app.config.from_object('app_config')
db = SQLAlchemy(app)

print "b"
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "users.login"

#FIXME: prob not the best place for this
def common_render(tmpl_name, **kwargs):
    common_args = {
        "user": current_user
    }

    kwargs.update(common_args)
    return render_template(tmpl_name, **kwargs)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.jinja'), 404
print "c"
@app.route('/')
def index():
    print "here"
    if current_user.is_anonymous:
        return common_render('splash.jinja')
    else:
        return common_render('dashboard.jinja')

print "d"
from app.users.views import mod as usersModule
app.register_blueprint(usersModule)
print "e"


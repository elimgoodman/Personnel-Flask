from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('app_config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "users.login"

#@app.errorhandler(404)
#def not_found(error):
    #return common_render('404.jinja'), 404

from app.users.views import mod as usersModule
app.register_blueprint(usersModule)

from app.people.views import mod as peopleModule
app.register_blueprint(peopleModule)

from app.index.views import mod as indexModule
app.register_blueprint(indexModule)

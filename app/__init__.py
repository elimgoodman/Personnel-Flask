from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

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

from app.api.views import mod as apiModule
app.register_blueprint(apiModule)

###ADMIN###

#admin_app = Admin(app, name="Personnel")
#from app.admin.views import IndexView
#from app.people.models import Person, Feedback, Note, Entry
#admin_app.add_view(ModelView(Person, db.session))
#admin_app.add_view(ModelView(Note, db.session))
#admin_app.add_view(ModelView(Entry, db.session))
#admin_app.add_view(ModelView(Feedback, db.session))

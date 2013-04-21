import os
from flask import Flask
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Hello World!'
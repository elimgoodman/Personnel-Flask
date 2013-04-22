import os
from os import environ
_basedir = os.path.abspath(os.path.dirname(__file__))

_local = {
    "PW_SALT": "$2a$12$0EqjsotuAMWiN63dRLsnMe",
    "DATABASE_URL": "sqlite:///test.db",
    "TOKEN_SECRET": "8qEJw9Nq63T3VZjvdugntU",
    "ENVIRONMENT": "development"
}

def get_config(key):
    if environ.has_key(key):
        return environ.get(key)
    else:
        return _local[key]

IS_PRODUCTION = get_config("ENVIRONMENT") == "production"

DEBUG = not IS_PRODUCTION

PW_SALT = get_config("PW_SALT")

SECRET_KEY = get_config("TOKEN_SECRET")

SQLALCHEMY_DATABASE_URI = get_config("DATABASE_URL")
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"



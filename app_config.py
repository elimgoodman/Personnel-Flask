import os
from os import environ
_basedir = os.path.abspath(os.path.dirname(__file__))

_dev = {
    "PW_SALT": "$2a$12$0EqjsotuAMWiN63dRLsnMe",
    "DATABASE_URL": "sqlite:///test.db",
    "TOKEN_SECRET": "8qEJw9Nq63T3VZjvdugntU",
    "registration_enabled": True
}

_prod = {
    "registration_enabled": False
}


def is_production():
    return environ.get("ENVIRONMENT") == "production"

def get_config(key):
    
    if environ.has_key(key):
        return environ.get(key)
    elif is_production() and _prod.has_key(key):
        return _prod[key]
    elif _dev.has_key(key):
        return _dev[key]
    else:
        raise Exception("Invalid config key: %s" % (key))

IS_PRODUCTION = is_production()

DEBUG = not IS_PRODUCTION

PW_SALT = get_config("PW_SALT")

SECRET_KEY = get_config("TOKEN_SECRET")

SQLALCHEMY_DATABASE_URI = get_config("DATABASE_URL")
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"

REGISTRATION_ENABLED = get_config("registration_enabled")

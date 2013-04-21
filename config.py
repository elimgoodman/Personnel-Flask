from os import environ

local = {
    "PW_SALT": "$2a$12$0EqjsotuAMWiN63dRLsnMe",
    "DATABASE_URL": "sqlite:///test.db",
    "TOKEN_SECRET": "8qEJw9Nq63T3VZjvdugntU"
}

def get_config(key):
    if environ.has_key(key):
        return environ.get(key)
    else:
        return local[key]

from app import app
app.run(debug=True)

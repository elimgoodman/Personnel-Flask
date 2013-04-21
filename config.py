from os import environ

local = {
    "PW_SALT": "$2a$12$0EqjsotuAMWiN63dRLsnMe",
    "DATABASE_URL": "sqlite:///test.db"
}

def get_config(key):
    if environ.has_key(key):
        return environ.get(key)
    else:
        return local[key]

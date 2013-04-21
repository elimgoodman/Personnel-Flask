import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'SecretKeyForSessionSigning'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'test.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'blahblahblahblahblahblahblahblahblah'
RECAPTCHA_PRIVATE_KEY = 'blahblahblahblahblahblahprivate'
RECAPTCHA_OPTIONS = {'theme': 'white'}

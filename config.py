import os

import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
    
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# available languages
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5


PING_INTERVAL = 5000
# PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=10)
# os.environ.get('HEROKU')
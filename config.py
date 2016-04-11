import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'dsvastberte4t345456bwe5bywertdsfgdfgd'

# postgresql://username:password@localhost/mydatabase
# mysql://username:password@localhost/mydatabase
# oracle+cx_oracle://username:password@127.0.0.1:1521/sidname
# sqlite:////absolute/path/to/foo.db

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# available languages
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}

# slow database query threshold (in seconds)
# DATABASE_QUERY_TIMEOUT = 0.5

# os.environ.get('HEROKU')

# pagination
NEWS_PER_PAGE = 5

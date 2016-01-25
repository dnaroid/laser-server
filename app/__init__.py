from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap3 import Bootstrap
from flask_babel import Babel, lazy_gettext


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
Bootstrap(app)
babel = Babel(app)


from app import views, models

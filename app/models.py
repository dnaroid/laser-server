from app import db
from hashlib import md5


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(10), unique=False)
    email = db.Column(db.String(50), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous():
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(
                self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.username)


from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30), unique=False)
    login = db.Column(db.String(30), unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(30), unique=True)
    expired = db.Column(db.TIMESTAMP)


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30), unique=True)


class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer,
                        db.ForeignKey('news.news_id', ondelete='CASCADE'),
                        nullable=False)
    comment_text = db.Column(db.String(100))
    creation_date = db.Column(db.TIMESTAMP)


class News(db.Model):
    __tablename__ = 'news'
    news_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    short_text = db.Column(db.String(100))
    full_text = db.Column(db.String(2000))
    creation_date = db.Column(db.TIMESTAMP)
    modification_date = db.Column(db.Date)
    comments = db.relationship('comments',
                               backref='comments',
                               lazy='dynamic')


class Role(db.Model):
    __tablename__ = 'roles'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


tags = db.Table('news_tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')),
                db.Column('news_id', db.Integer, db.ForeignKey('news.news_id'))
                )

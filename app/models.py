from app import db

news_tag = db.Table('news_tag',
                    db.Column('tag_id',
                              db.Integer,
                              db.ForeignKey('tag.tag_id')),
                    db.Column('news_id',
                              db.Integer,
                              db.ForeignKey('news.news_id')))

news_author = db.Table('news_author',
                       db.Column('author_id',
                                 db.Integer,
                                 db.ForeignKey('author.author_id')),
                       db.Column('news_id',
                                 db.Integer,
                                 db.ForeignKey('news.news_id')))


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
        return self.user_id

    def verify_password(self, passw):
        return self.password == passw

    def __repr__(self):
        return '<User %r>' % self.user_name


class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(30), unique=True)
    expired = db.Column(db.TIMESTAMP)

    def get_author_name(self):
        return self.author_name

    @staticmethod
    def get_all_actual_list():
        return Author.query \
            .with_entities(Author.author_id, Author.author_name) \
            .filter(Author.expired.is_(None)) \
            .order_by('author_name') \
            .all()

    @staticmethod
    def get_all_active():
        return Author.query \
            .with_entities(Author.author_id, Author.author_name) \
            .join(news_author) \
            .filter(news_author.c.author_id == Author.author_id) \
            .order_by('author_name') \
            .all()


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return '<Tag %r: %r>' % (self.tag_id, self.tag_name)

    @staticmethod
    def get_all_list():
        return Tag.query \
            .with_entities(Tag.tag_id, Tag.tag_name) \
            .order_by('tag_name') \
            .all()


class News(db.Model):
    __tablename__ = 'news'
    news_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    short_text = db.Column(db.String(100))
    full_text = db.Column(db.String(2000))
    creation_date = db.Column(db.TIMESTAMP)
    modification_date = db.Column(db.Date)
    comments = db.relationship('Comments', backref="author", lazy='dynamic')

    author = db.relationship('Author', secondary=news_author,
                             primaryjoin=(news_author.c.news_id == news_id),
                             secondaryjoin=(
                                 news_author.c.author_id == Author.author_id),
                             backref=db.backref('author', lazy='dynamic'),
                             lazy='dynamic')
    tags = db.relationship('Tag', secondary=news_tag,
                           primaryjoin=(news_tag.c.news_id == news_id),
                           secondaryjoin=(news_tag.c.tag_id == Tag.tag_id),
                           backref=db.backref('tags', lazy='dynamic'),
                           lazy='dynamic')

    def set_author(self):
        ...

    def get_comments(self):
        return Comments.query.filter(Comments.news_id == self.news_id).all()

    def get_comments_list(self):
        return Comments.query \
            .with_entities(Comments.comment_id, Comments.creation_date,
                           Comments.comment_text, Comments.news_id) \
            .filter(Comments.news_id == self.news_id).all()

    def get_comments_count(self):
        return Comments.query.filter(Comments.news_id == self.news_id).count()

    def get_author(self):
        return Author.query.join(news_author, (
            news_author.c.author_id == Author.author_id)).filter(
            news_author.c.news_id == self.news_id).first()

    def get_tags(self):
        res = Tag.query \
            .with_entities(Tag.tag_name) \
            .join(news_tag, (news_tag.c.tag_id == Tag.tag_id)) \
            .filter(news_tag.c.news_id == self.news_id).all()
        return ', '.join(r[0] for r in res)

    @staticmethod
    def get_by_id(id):
        return News.query.filter(News.news_id == id).first()

    @staticmethod
    def get_news_list(page=0):
        return News.query \
            .with_entities(News.news_id, News.title) \
            .order_by(News.creation_date) \
            .all()

    def __repr__(self):
        return '<News %r: %r>' % (self.news_id, self.title)


class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'))
    comment_text = db.Column(db.String(100))
    creation_date = db.Column(db.TIMESTAMP)


class Role(db.Model):
    __tablename__ = 'roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        primary_key=True)
    name = db.Column(db.String(50))

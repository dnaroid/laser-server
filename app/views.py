from flask import request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from sqlalchemy import func

from app import app, db, lm
from app.models import News, Author, Tag, User, news_author, news_tag, Comments
from config import NEWS_PER_PAGE


@app.route('/_login', methods=['POST'])
def _login():
    form = request.form
    login_ = form.getlist('login')[0]
    password = form.getlist('password')[0]
    user = User.query.filter_by(login=login_).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        return jsonify({
            'login': 'ok',
            'user': user.user_name})
    else:
        return jsonify({'login': 'error'})


@app.route('/_add_news', methods=['GET', 'POST'])
@login_required
def _add_news():
    json = request.get_json(force=True)
    print(json)
    news = News(title=json['title'], short_text=json['short_text'],
                full_text=json['full_text'],
                )
    from datetime import datetime
    news.creation_date = datetime.strptime(json['creation_date'], '%d/%m/%Y')
    tag_list = json['tags']
    author_id = json['author_id']
    author = Author.query \
        .filter(Author.author_id == author_id)
    news.author = author
    tags = Tag.query \
        .filter(Tag.tag_id.in_(tag_list)).all()
    news.tags = tags
    db.session.add(news)
    db.session.commit()
    return 'ok'


@app.route('/_del_news', methods=['GET', 'POST'])
@login_required
def _del_news():
    json = request.get_json(force=True)
    news_id_list = json['id']
    News.query.filter(News.news_id.in_(news_id_list)).delete(
        synchronize_session=False)
    db.session.commit()
    return 'ok'


@app.route('/_update_author', methods=['GET', 'POST'])
@login_required
def _update_author():
    json = request.get_json(force=True)
    id = json['id']
    name = json['new_name']
    author = Author.query.filter(Author.author_id == id).first()
    author.author_name = name
    db.session.commit()
    return 'ok'


@app.route('/_update_tag', methods=['GET', 'POST'])
@login_required
def _update_tag():
    json = request.get_json(force=True)
    id = json['id']
    name = json['new_name']
    tag = Tag.query.filter(Tag.tag_id == id).first()
    tag.tag_name = name
    db.session.commit()
    return 'ok'


@app.route('/_expire_author', methods=['GET', 'POST'])
@login_required
def _expire_author():
    json = request.get_json(force=True)
    id = json['id']
    author = Author.query.filter(Author.author_id == id).first()
    author.expired = func.current_timestamp()
    db.session.commit()
    return 'ok'


@app.route('/_del_tag', methods=['GET', 'POST'])
@login_required
def _del_tag():
    json = request.get_json(force=True)
    id = json['id']
    Tag.query.filter(Tag.tag_id == id).delete(synchronize_session=False)
    db.session.commit()
    return 'ok'


@app.route('/_del_comment', methods=['GET', 'POST'])
@login_required
def _del_comment():
    id = request.args['id']
    Comments.query.filter(Comments.comment_id == id).delete(
        synchronize_session=False)
    db.session.commit()
    return 'ok'


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(LANGUAGES.keys())


# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     todo
#     user = User(username=username, password=password, email=email)
#     db.session.add(user)
#     db.session.commit()
#     login_user(user)
#     return redirect(url_for('/'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/_logout')
def _logout():
    logout_user()
    return 'ok'


@app.route('/_get_news')
def _get_news():
    id = request.values['id']
    news = News.get_by_id(id)
    comm = news.get_comments_list()
    res = {
        'id': news.news_id,
        'title': news.title,
        'author': news.get_author().author_name,
        'text': news.full_text,
        'comments': comm,
        'date': news.creation_date}
    return jsonify(res)


@app.route('/_get_all_tags')
def _get_all_tags():
    return jsonify(Tag.get_all_list())


@app.route('/_get_all_authors')
def _get_all_authors():
    return jsonify(Author.get_all_actual_list())


@app.route('/_get_active_authors')
def _get_active_authors():
    return jsonify(Author.get_all_active())


@app.route('/_add_comment', methods=['GET', 'POST'])
def _add_comment():
    json = request.get_json(force=True)
    news_id = json['news_id']
    text = json['text']
    comment = Comments()
    comment.comment_text = text
    comment.creation_date = func.current_timestamp()
    comment.news_id = news_id
    db.session.add(comment)
    db.session.flush()
    new_id = comment.comment_id
    db.session.commit()
    return '{"new_id":"' + str(new_id) + '"}'


@app.route('/_add_author', methods=['GET', 'POST'])
def _add_author():
    json = request.get_json(force=True)
    name = json['name']
    author = Author()
    author.author_name = name
    db.session.add(author)
    db.session.flush()
    new_id = author.author_id
    db.session.commit()
    return '{"new_id":"' + str(new_id) + '"}'


@app.route('/_add_tag', methods=['GET', 'POST'])
def _add_tag():
    json = request.get_json(force=True)
    name = json['name']
    tag = Tag()
    tag.tag_name = name
    db.session.add(tag)
    db.session.flush()
    new_id = tag.tag_id
    db.session.commit()
    return '{"new_id":"' + str(new_id) + '"}'


@app.route('/_get_news_list/<int:page>', methods=['GET', 'POST'])
def _get_news_list(page=0):
    pagin = News.query \
        .order_by(News.creation_date) \
        .paginate(page, NEWS_PER_PAGE, False)
    return get_json(pagin)


@app.route('/_get_news_list_by_author/<int:page>', methods=['GET', 'POST'])
def _get_news_list_by_author(page=0):
    json = request.get_json(force=True)
    id = json['author']
    print(id)
    pagin = News.query \
        .join(news_author) \
        .filter_by(author_id=id) \
        .order_by(News.creation_date) \
        .paginate(page, NEWS_PER_PAGE, False)
    return get_json(pagin)


@app.route('/_get_news_list_by_tags/<int:page>', methods=['GET', 'POST'])
def _get_news_list_by_tags(page=0):
    json = request.get_json(force=True)
    tags = json['tags']
    pagin = News.query \
        .join(news_tag) \
        .filter(news_tag.c.tag_id.in_(tags)) \
        .order_by(News.creation_date) \
        .paginate(page, NEWS_PER_PAGE, False)
    return get_json(pagin)


@app.route('/_get_news_list_by_author_and_tags/<int:page>',
           methods=['GET', 'POST'])
def _get_news_list_by_author_and_tags(page=0):
    json = request.get_json(force=True)
    author = json['author']
    tags = json['tags']
    pagin = News.query \
        .join(news_author) \
        .filter(news_author.c.author_id == author) \
        .join(news_tag) \
        .filter(news_tag.c.tag_id.in_(tags)) \
        .order_by(News.creation_date) \
        .paginate(page, NEWS_PER_PAGE, False)
    return get_json(pagin)


def get_json(pagin):
    items = pagin.items
    pages = pagin.pages
    page = pagin.page
    data = []
    for news in items:
        data.append({
            'id': news.news_id,
            'title': news.title,
            'author': news.get_author().author_name,
            'short': news.short_text,
            'tags': news.get_tags(),
            'comments': news.get_comments_count(),
            'date': news.creation_date})
    res = {
        'num_pages': pages,
        'current_page': page,
        'news_list': data}
    return jsonify(res)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return app.send_static_file('index.html')

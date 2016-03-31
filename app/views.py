from flask import render_template, flash, redirect, url_for, request, session
from sqlalchemy import func

from app import app, db, babel
from app.forms import AddNewsForm, FilterForm
from app.models import News, news_author, Author, Tag, news_tag
from config import LANGUAGES, NEWS_PER_PAGE


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.is_submitted() and form.validate:
#         user = User.query.filter_by(login=form.login.data).first()
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user, form.remember_me.data)
#             flash('Logged in successfully', category='success')
#             return redirect(request.args.get('next') or url_for('index'))
#         flash('Invalid username or password.', category='error')
#     return render_template('login.html', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    if form.is_submitted() and form.validate:
        news = News(title=form.title.data, short_text=form.short_text.data,
                    full_text=form.full_text.data,
                    creation_date=func.current_timestamp())
        db.session.add(news)
        db.session.commit()
        flash('News added successfully', category='success')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('add_news.html', form=form)


# @app.route('/list_news', methods=['GET', 'POST'])
# def list_news():
#     list = News.query.order_by(News.creation_date)
#     return render_template('index.html', list=list)


# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     todo
#     user = User(username=username, password=password, email=email)
#     db.session.add(user)
#     db.session.commit()
#     flash('Registration succesfull', category='success')
#     login_user(user)
#     return redirect(url_for('/'))


# @app.before_request
# def before_request():
#     g.user = current_user


# @app.route('/logout')
# def logout():
#     logout_user()
#     flash('Logged out successfully', category='success')
#     return redirect(url_for('index'))


# @app.route('/user/<username>')
# @app.route('/user/<username>/<int:page>')
# @login_required
# def user(username, page=1):
#     user = User.query.filter_by(user_name=username).first()
#     if user is None:
#         flash('User ' + username + ' not found.', category='danger')
#         return redirect(url_for('index'))
#     return render_template('user.html', user=user)


@app.route('/news/<string:back>/<int:id>', methods=['GET', 'POST'])
def show_news(id, back):
    news = News.get_by_id(id)
    return render_template('show_news.html', news=news, back=back)


# news list
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    form = FilterForm()
    if 'author' not in session.keys():
        session['author'] = '0'
    if 'tags' not in session.keys():
        session['tags'] = []
    args = request.args
    if 'reset' in args.keys():
        session['author'] = '0'
        session['tags'] = []
    elif 'filter' in args.keys():
        session['author'] = args['author']
        session['tags'] = [int(t) for t in args.getlist('tags')]
    return render_template('index.html', list=get_news_page(page), form=form,
                           authors=Author.get_all_actual(), tags=Tag.get_all(),
                           sel_tags=session['tags'],
                           author=int(session['author']))


def get_news_page(page):
    no_author = session['author'] == '0'
    no_tags = session['tags'] == []
    if no_author and no_tags:  # no filters
        return News.query \
            .order_by(News.creation_date) \
            .paginate(page, NEWS_PER_PAGE, False)
    if no_tags:  # only author filter
        return News.query \
            .join(news_author, (news_author.c.news_id == News.news_id)) \
            .filter(news_author.c.author_id == session['author']) \
            .order_by(News.creation_date) \
            .paginate(page, NEWS_PER_PAGE, False)
    if no_author:  # only tag filter
        return News.query \
            .join(news_tag, (news_tag.c.news_id == News.news_id)) \
            .filter(news_tag.c.tag_id.in_(session['tags'])) \
            .order_by(News.creation_date) \
            .paginate(page, NEWS_PER_PAGE, False)
    # author & tag filters
    return News.query \
        .join(news_author, (news_author.c.news_id == News.news_id)) \
        .filter(news_author.c.author_id == session['author']) \
        .join(news_tag, (news_tag.c.news_id == News.news_id)) \
        .filter(news_tag.c.tag_id.in_(session['tags'])) \
        .order_by(News.creation_date) \
        .paginate(page, NEWS_PER_PAGE, False)

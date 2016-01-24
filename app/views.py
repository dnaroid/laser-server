import re

from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from models import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime
from flask_babel import gettext as _


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    username = re.sub('[^a-zA-Z0-9_\.]', '', username)
    password = request.form['password']
    password2 = request.form['password2']
    email = request.form['email']
    u = User.query.filter_by(username=username).first()
    if len(username) < 4:
        flash(_('Name too short, 4 is minimal length!'), category='danger')
        return redirect(url_for('register'))
    if u is not None:
        flash(_('Nickname aleady in use!'), category='danger')
        return redirect(url_for('register'))
    if len(password) < 4:
        flash('Password too short, 4 is minimal length!', category='danger')
        return redirect(url_for('register'))
    if len(password) > 10:
        flash('Password too long, 10 is maximal length!', category='danger')
        return redirect(url_for('register'))
    if password != password2:
        flash('Check password error!', category='danger')
        return redirect(url_for('register'))
    if len(email) < 4:
        flash('Enter valid email!', category='danger')
        return redirect(url_for('register'))
    user = User(username=username, password=password, email=email,
                role=ROLE_USER)
    db.session.add(user)
    db.session.commit()
    flash('Registration succesfull', category='success')
    login_user(user)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username,
                                           password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'danger')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully', category='success')
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User ' + username + ' not found.', category='success')
        return redirect(url_for('index'))
    return render_template('user.html', last_seen="", user=user)

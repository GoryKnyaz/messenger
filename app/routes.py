import requests
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_moment import moment
from werkzeug.urls import url_parse
from app import app, db, Config
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, EmptyForm
from app.models import User, Post
from datetime import datetime


# from bs4 import BeautifulSoup


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).limit(Config.POSTS_PER_PAGE).all()[::-1]
    return render_template('index.html', title='Messenger', form=form,
                           posts=posts)

@app.route('/sendMessage', methods=['GET'])
@login_required
def sendMessage():
    user_name = request.args.get('user')
    timestamp = datetime.utcfromtimestamp(datetime.fromisoformat(request.args.get('time')).timestamp())
    body = request.args.get('body')
    last_user = User.query.filter_by(username=user_name).first()
    post = db.session.query(Post).filter(Post.user_id == last_user.id, Post.body == body,
                                         Post.timestamp.like('%{}%'.format(timestamp))).first()
    post_id = 0 if post is None else post.id
    posts = db.session.query(Post).filter(Post.id > post_id).order_by(Post.timestamp.asc()).all()
    post = Post(body=request.args.get('cur_body'), author=current_user)
    db.session.add(post)
    db.session.commit()
    posts.append(post)
    return render_template('posts.html', posts=posts)


@app.route('/whatNews')
def whatNews():
    user_name = request.args.get('user')
    timestamp = datetime.utcfromtimestamp(datetime.fromisoformat(request.args.get('time')).timestamp())
    body = request.args.get('body')
    last_user = User.query.filter_by(username=user_name).first()
    post = db.session.query(Post).filter(Post.user_id == last_user.id, Post.body == body,
                                         Post.timestamp.like('%{}%'.format(timestamp))).first()
    post_id = 0 if post is None else post.id
    posts = db.session.query(Post).filter(Post.id > post_id).order_by(Post.timestamp.asc()).all()
    return render_template('posts.html', posts=posts)


@app.route('/explore')
@login_required
def explore():
    posts = current_user.followed_posts().all()
    return render_template("index.html", title='Explore', posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, title=f"{username}", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

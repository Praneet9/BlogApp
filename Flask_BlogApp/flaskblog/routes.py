from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, bcrypt, mail
from flaskblog.models import User, Post, User_Model
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.db import (register_user, check_user, updateAccount, newPost,
                          fetchPosts, getPost, updatePost, deletePost,
                          fetchUserPosts, updatePassword)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flaskblog.utils import save_picture, iter_pages
import math


@app.route('/')
@app.route('/home')
def home():
    total_cards = 5
    page = request.args.get('page', 1, type=int)
    posts = fetchPosts(page=page, total_cards=total_cards)
    if (page - 1) * total_cards >= posts.count():
        abort(404)
    else:
        n_pages = math.ceil(posts.count() / total_cards)
        pagination = list(iter_pages(pages=n_pages, page=page))
        return render_template(
            'home.html', posts=posts, pagination=pagination, page=page)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    except:
        pass
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        register_user(user)
        flash('Your account has been created! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    except:
        pass
    form = LoginForm()
    if form.validate_on_submit():
        user = check_user(form.email.data)
        if user and bcrypt.check_password_hash(user['password'],
                                               form.password.data):
            user_model = User_Model(user)
            login_user(user_model)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = current_user.image_file
        old = {
            'username': current_user.username,
            'email': current_user.email,
            'image_file': current_user.image_file
        }
        new = {
            'username': form.username.data,
            'email': form.email.data,
            'image_file': picture_file
        }
        updateAccount(old, new)
        current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data

        flash("Your account has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template(
        'account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        newPost(post)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template(
        'create_post.html', title='New Post', form=form, legend='New Post')


@app.route('/post/<post_id>')
def post(post_id):
    post = getPost(post_id)
    if not post:
        abort(404)
    return render_template('post.html', title=post['title'], post=post)


@app.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = getPost(post_id)
    if not post:
        abort(404)
    if post['author'] != current_user.username:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post['title'] = form.title.data
        post['content'] = form.content.data
        updatePost(post_id=post_id, updated_post=post)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post['_id']))
    elif request.method == 'GET':
        form.title.data = post['title']
        form.content.data = post['content']
    return render_template(
        'create_post.html',
        title='Update Post',
        form=form,
        legend='Update Post')


@app.route('/post/<post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = getPost(post_id)
    if not post:
        abort(404)
    if post['author'] != current_user.username:
        abort(403)
    deletePost(post_id)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
    total_cards = 5
    page = request.args.get('page', 1, type=int)
    posts = fetchUserPosts(
        username=username, page=page, total_cards=total_cards)
    if not posts or posts.count() == 0:
        abort(404)
    else:
        n_pages = math.ceil(posts.count() / total_cards)
        pagination = list(iter_pages(pages=n_pages, page=page))
        return render_template(
            'user_posts.html',
            posts=posts,
            pagination=pagination,
            page=page,
            user=username)


def send_reset_email(user):
    token = user.get_reset_token()
    print(user.email)
    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email])
    msg.body = '''To reset your password, visit the following link: ''' + url_for(
        'reset_token', token=token, _external=True) + '''\n
        If you did not make this request then simply ingore this email and no changes will be made.
        '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    except:
        pass
    form = RequestResetForm()
    if form.validate_on_submit():
        user = check_user(form.email.data)
        user_model = User_Model(user)
        send_reset_email(user_model)
        flash(
            'An email has been sent with instructions to reset your password',
            'info')
        return redirect(url_for('login'))
    return render_template(
        'reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    except:
        pass
    user = User_Model.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        old = {
            'username': user.username,
            'email': user.email,
        }
        new = {
            'username': user.username,
            'email': user.email,
            'password': hashed_password
        }
        updatePassword(old, new)
        flash('Your password has been updated! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template(
        'reset_token.html', title='Reset Password', form=form)


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, bcrypt
from flaskblog.models import User, Post, User_Model
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.db import register_user, check_user
from flask_login import login_user, current_user, logout_user, login_required

posts = [{
    'author': 'Praneet Bomma',
    'title': 'First Post',
    'date_posted': 'April 8, 2019',
    'content': 'This is my first post'
},
         {
             'author': 'Jane Doe',
             'title': 'Second Post',
             'date_posted': 'April 9, 2019',
             'content': 'This is the second post'
         }]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        register_user(user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login')) 
    return render_template('register.html', title='Register', form = form)


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
        user_model = User_Model(user)
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            login_user(user_model)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title = 'Account')
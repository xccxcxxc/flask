from flask import render_template, send_from_directory, flash, redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app,db
from app.models import User
from app.forms import LoginForm, RegistrationForm
import logging

#logging.basicConfig(level=logging.INFO,
                    #format='%(asctime)s - %(levelname)s: %(message)s')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - [%(funcName)s]: %(message)s')

@app.route('/feed')
def feed():
    # 提供 rss_feed.xml 文件
    return send_from_directory('templates', 'rss_feed.xml')

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        #logging.info(f'Username: {form.username.data}, nextpage:{request.args.get("next")}, user: {user}')
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    else:
        logging.error(f'{form.errors}')
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    #logging.info(f'current_user: {current_user}')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    #logging.info(f'Validata: {form.validate_on_submit()} Username: {form.username.data}')
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, yu are now a registered user!')
        return redirect(url_for('login'))
    else:
        logging.error(f'{form.errors}')
    return render_template('register.html', title='Register', form=form)


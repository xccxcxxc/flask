from flask import render_template, send_from_directory, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/feed')
def feed():
    # 提供 rss_feed.xml 文件
    return send_from_directory('templates', 'rss_feed.xml')

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'cc'}
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
    return render_template('index.html', title='Home', user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Lgin requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)
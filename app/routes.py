from flask import render_template, send_file, send_from_directory
from app import app

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

@app.route('/feed')
def feed():
    # 提供 rss_feed.xml 文件
    return send_from_directory('templates', 'rss_feed.xml')

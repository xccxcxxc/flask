from flask import render_template, send_file, send_from_directory
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/feed')
def feed():
    # 提供 rss_feed.xml 文件
    return send_from_directory('templates', 'rss_feed.xml')

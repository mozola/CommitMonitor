import flask

from flask import render_template

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('base/index.html')


@app.route('/login')
def login():
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    return render_template('auth/logout.html')


@app.route('/register')
def register():
    return render_template('auth/register.html')


@app.route('/repository/add')
def add_repository():
    return render_template('repository/new.html')


@app.route('/repository/display')
def display_repository():
    return render_template('repository/display.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
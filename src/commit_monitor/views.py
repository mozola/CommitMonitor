from flask import Flask
from flask import render_template, url_for
from flask import session
from flask import request, redirect
from flask import url_for
import requests

from bs4 import BeautifulSoup
from .http_handler import Repository, Repositories


app = Flask(__name__)

""" Temporary configuration added to views """
app.config.update(
    SECRET_KEY=b'123',
    DEBUG=False,
    TESTING=False,
    PROPAGATE_EXCEPTIONS=None,
)


""" Temporary dictionary to login user """
USER_DATE = {'username': 'admin',
             'password': 'admin'}


""" All subscribed repositories """
all_repositories = Repositories()


@app.route('/')
def index():
    """
        Major page of project
    """
    return render_template('base/index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
        View to login user and setup session
    """
    if request.method == 'POST':
        if (request.form['username'] == USER_DATE['username']
            and request.form['password'] == USER_DATE['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    """
        Logout user and remove him from session
    """
    session.pop('username', None)
    return render_template('auth/logout.html')


@app.route('/register')
def register():
    return render_template('auth/register.html')


@app.route('/repository/add', methods=['POST', 'GET'])
def add_repository():
    if request.method == 'POST':
        repository = Repository(request.form['name'],
                                request.form['url'],
                               )
        all_repositories.add(repository)
        return render_template('repository/display.html',
                                repository=repository,
                              )
    return render_template('repository/new.html')


@app.route('/repository/subscribed')
def subscribed():
    return render_template('repository/subscribed.html',
                           repositories = all_repositories._container)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.route('/repository/commits')
def commits():
    return render_template('repository/commits.html',
                           repositories = all_repositories._container)

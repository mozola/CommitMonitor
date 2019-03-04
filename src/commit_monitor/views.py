from flask import Flask
from flask import render_template
from flask import session
from flask import request, redirect
from flask import url_for

from datetime import timedelta

from .http_handler import Repository, Repositories


app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SECRET_KEY'] = b'123'

""" Temporary configuration added to views """
app.config.update(
    SECRET_KEY=b'123',
    DEBUG=False,
    TESTING=False,
    PROPAGATE_EXCEPTIONS=None,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=5),
)


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SECRET_KEY'] = b'123'


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


@app.route('/auth/login', methods=['POST', 'GET'])
def login():
    """
        View to login user and setup session
    """
    if request.method == 'POST':
        if (request.form['username'] == USER_DATE['username']
                and request.form['password'] == USER_DATE['password']):
            session['username'] = request.form['username']
            session.permanent = True
            return redirect(url_for('index'))

    return render_template('auth/login.html')


@app.route('/auth/logout')
def logout():
    """
        Logout user and remove him from session
    """
    session.pop('username', None)
    return render_template('auth/logout.html')


@app.route('/auth/register')
def register():
    return render_template('auth/register.html')


@app.route('/repository/add', methods=['POST', 'GET'])
def add_repository():
    if request.method == 'POST':
        repository = Repository(name=request.form['name'],
                                url=request.form['url'])

        if repository.name not in [i.name for i in all_repositories.container]:
            all_repositories.add(repository)

        return render_template('repository/new.html', state=False,
                               repositories=all_repositories._container)

    return render_template('repository/new.html', state=True)


@app.route('/repository/subscribed')
def subscribed():
    return render_template('repository/subscribed.html',
                           repositories=all_repositories._container)


@app.route('/repository/modify')
def modify():
    return render_template('repository/modify.html')


@app.route('/repository/commits')
def commits():
    return render_template('repository/commits.html',
                           repositories=all_repositories._container)


@app.route('/statistics/projects', methods=['POST', 'GET'])
def statistics_project():
    repositories = all_repositories._container
    if request.method == 'POST':
        project_name = request.form['project_name']
        print(repositories)
        return render_template('statistics/projects.html',
                               repositories=repositories,
                               project_name=project_name)
    return render_template('statistics/projects.html',
                           repositories=repositories)


@app.route('/statistics/user', methods=['POST', 'GET'])
def statistics_user():
    repositories = all_repositories._container
    if request.method == 'POST':
        user = request.form['username']
        return render_template('statistics/user.html',
                               repositories=repositories,
                               user=user)
    return render_template('statistics/user.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

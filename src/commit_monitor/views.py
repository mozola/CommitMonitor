from flask import (Flask, render_template,
                   session, request,
                   redirect, url_for, abort)

from datetime import timedelta

from .auth import User
from .http_handler import Repository, Repositories


app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SECRET_KEY'] = b'123'


""" All subscribed repositories """
all_repositories = Repositories()


@app.route('/')
def index():
    return render_template('base/index.html')


# Authorisation and register user


@app.route('/auth/login', methods=['POST', 'GET'])
def login():
    user = User()
    state = True
    if request.method == 'POST':

        if user.validate(request.form['username'],
                         request.form['password']):

            session['username'] = user.username
            session.permanent = True
            return redirect(url_for('index'))
        state = False

    return render_template('auth/login.html', state=state)


@app.route('/auth/logout')
def logout():
    session.pop('username', None)
    return render_template('auth/logout.html')


@app.route('/auth/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        user = User()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        login = request.form['login']

        state = user.add(username, password, login, email)
        if state:
            return redirect(url_for('index'))
        else:
            abort(401)

    return render_template('auth/register.html')


# All about repositories


@app.route('/repository/add', methods=['POST', 'GET'])
def repository_subscribe():
    if request.method == 'POST':
        repository = Repository(name=request.form['name'],
                                url=request.form['url'])

        if repository.name not in [i.name for i in all_repositories.container]:
            all_repositories.add(repository)

        return render_template('repository/repository_subscribe.html', state=False,
                               repositories=all_repositories._container)

    return render_template('repository/repository_subscribe.html', state=True)


@app.route('/repository/subscribed', methods=['POST', 'GET'])
def repository_subscribed():
    return render_template('repository/repository_subscribed.html',
                           repositories=all_repositories._container)


@app.route('/repository/merge_requests')
def repository_merge_requests():
    return render_template('repository/repository_merge_requests.html')


@app.route('/repository/labels')
def repository_labels():
    return render_template('repository/repository_labels.html')


@app.route('/repository/workflows')
def repository_workflows():
    return render_template('repository/repository_workflows.html')


@app.route('/repository/issues')
def repository_issues():
    return render_template('repository/repository_issues.html',
                           repositories=all_repositories._container)


@app.route('/repository/commits', methods=['POST', 'GET'])
def repository_commits():
    repositories = all_repositories._container
    if request.method == 'POST':
        project_name = request.form['project_name']
        return render_template('repository/repository_commits.html',
                               repositories=repositories,
                               project_name=project_name)
    return render_template('repository/repository_commits.html',
                           repositories=repositories)


# Statistics about project


@app.route('/statistics/user', methods=['POST', 'GET'])
def statistics_user():
    repositories = all_repositories._container
    if request.method == 'POST':
        user = request.form['username']
        return render_template('statistics/user.html',
                               repositories=repositories,
                               user=user)
    return render_template('statistics/user.html')


# Teams and users


@app.route('/users/teams/all')
def users_teams():
    return render_template('users/teams_all.html')


@app.route('/users/teams/users')
def users_users():
    return render_template('users/teams_user.html')


@app.route('/users/teams/new')
def users_new_team():
    return render_template('/users/teams_form.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(401)
def authorisation_error(e):
    return render_template('errors/401.html'), 401

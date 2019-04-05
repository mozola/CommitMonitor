import requests

from bs4 import BeautifulSoup
from .auth import DATABASE

REGEXES = {'commit_names':
           ('a', {'class': 'message js-navigation-open'}),
           'commit_auth':
           ('a',
            {'class':
             'commit-author tooltipped tooltipped-s user-mention'}),
           'commit_date': ('relative-time'),
           'branches_names':
           ('a', {'class':
                  'branch-name css-truncate-target v-align-'
                  'baseline width-fit mr-2 Details-content--shown'}),
           'branches_users': ('a', {'class': 'muted-link'}),
           }


GITLAB_REGEXES = {'commit_names':
                  ('a', {'class': 'commit-row-message item-title'}),
                  'commit_auth':
                  ('a', {'class': 'commit-author-link has-tooltip'}),
                  'branches_names':
                  ('a', {'class': 'item-title str-truncated ref-name'}),
                  'branches_users': ('a', {'class': 'muted-link'}),
                  }


class Commit:

    def __init__(self, auth, name, date):
        self._auth = auth
        self._date = date
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def auth(self):
        return self._auth

    @property
    def date(self):
        return self._date

    def setup_author(self):
        pass

    def add_commit(self, branch):
        pass


class Branch:

    def __init__(self, name, auth, url):
        self._name = name
        self._auth = auth
        self._commits = list(self.setup_commits(url, name))

    @property
    def name(self):
        return self._name

    @property
    def auth(self):
        return self._auth

    @property
    def commits(self):
        return self._commits

    def setup_commits(self, url, name):
        resp = requests.get('{}/commits/{}'.format(url, name))
        soup = BeautifulSoup(resp.text)
        names = soup.find_all(*REGEXES['commit_names'])
        auths = soup.find_all(*REGEXES['commit_auth'])
        dates = soup.find_all('relative-time')
        for name, auth, date in zip(names, auths, dates):
            yield Commit(name=name.text, auth=auth.text, date=date.text)


class Repository:

    def __init__(self, name=None, url=None, rtype=REGEXES, state=True):
        self._name = name
        self._state = state
        self._url = url
        self._rtype = rtype
        self._branches = list(self.setup_branches(url))

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def branches(self):
        return self._branches

    def setup_branches(self, url):
        resp = requests.get(url + '/branches/')
        soup = BeautifulSoup(resp.text)
        branches = soup.findAll(*self._rtype['branches_names'])
        users = soup.findAll(*self._rtype['branches_users'])
        for branch, auth in zip(branches, users):
            yield Branch(name=branch.text, auth=auth.text, url=self.url)

    def __repr__(self):
        return f'<repository> {self.name}, {self.url}'

    def dict(self):
        return {'name': self.name, 'url': self.url}


class Repositories:

    def __init__(self):
        self._container = []
        self._database = DATABASE['subscribes']

    def add(self, repository):
        self._container.append(repository)

    @property
    def container(self):
        return self._container

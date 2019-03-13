import requests
import abc
from enum import Enum

from bs4 import BeautifulSoup


class User(Enum):
    username = 'molo226'
    password = 'atb7jwnd'


class RepositoryInterface(metaclass=abc.ABCMeta):

    def __init__(self, url: str):
        self._url = url
        self._username = User.username
        self._password = User.password

    @property
    def url(self):
        return self._url

    @property
    def username(self):
        return self._username

    @abc.abstractmethod
    def get_commits(self):
        return NotImplementedError

    @abc.abstractmethod
    def get_branches(self):
        return NotImplementedError

    @abc.abstractmethod
    def get_requests(self):
        return NotImplementedError


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

    def setup_commits(self, url, name):
        resp = requests.get('{}/commits/{}'.format(url, name))
        soup = BeautifulSoup(resp.text)
        names = soup.find_all(*REGEXES['commit_names'])
        auths = soup.find_all(*REGEXES['commit_auth'])
        dates = soup.find_all('relative-time')
        for name, auth, date in zip(names, auths, dates):
            yield Commit(name=name.text, auth=auth.text, date=date.text)


class Repository(RepositoryInterface):

    def __init__(self, url=None):
        super().__init__(url=url)

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


class Repositories:

    def __init__(self):
        self._container = []

    def add(self, repository):
        self._container.append(repository)

    @property
    def container(self):
        return self._container

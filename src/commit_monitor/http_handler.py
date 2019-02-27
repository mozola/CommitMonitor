import abc
import requests

from bs4 import BeautifulSoup


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
        names = soup.find_all('a', {'class': 'message js-navigation-open'})
        auths = soup.find_all('a', {'class': 'commit-author tooltipped tooltipped-s user-mention'})
        dates = soup.find_all('relative-time')
        for name, auth, date in zip(names, auths, dates):
            yield Commit(name=name.text, auth=auth.text, date=date.text)


class Repository:

    def __init__(self, name=None, url=None):
        self._name = name
        self._url = url
        self._branches = list(self.setup_branches(url))

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def branches(self) ->list:
        return self._branches

    def setup_branches(self, url)-> Branch:
        resp = requests.get(url + '/branches/')
        soup = BeautifulSoup(resp.text)
        branches = soup.findAll('a', {'class': 'branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown'})
        users = soup.findAll('a', {'class': 'muted-link'})
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


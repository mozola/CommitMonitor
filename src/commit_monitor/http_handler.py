import abc
import requests

from bs4 import BeautifulSoup


class Repository:

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
        self.branch = None
        self.commits = None

    def _get_commits(self, branch):
        resp = requests.get('{}/commits/{}'.format(self.url, branch))
        soup = BeautifulSoup(resp.text)
        for i in soup.find_all('a', {'class': 'message js-navigation-open'}):
            yield i.attrs['title']

    def get_commits(self, branch):
        return list(self._get_commits(branch))

    def get_users(self):
        pass


class Repositories:

    def __init__(self):
        self._container = []

    def get_branches(self, url):
        resp = requests.get(url + '/branches/')
        soup = BeautifulSoup(resp.text)
        for i in soup.findAll('div', {'class': 'branch-summary js-branch-row'}):
            yield i.attrs['data-branch-name']

    def add(self, repository):
        for branch in self.get_branches(repository.url):
            print(branch)
            repo = Repository(repository.name, repository.url)
            repo.branch = branch
            repo.commits = repository.get_commits(branch)
            self._container.append(repo)
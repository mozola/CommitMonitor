import abc
import requests

from bs4 import BeautifulSoup


class Repository:

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
        self.branches = self.get_branches()
        self.commits = None

    def _get_branches_names(self):
        resp = requests.get(self.url + '/branches/')
        soup = BeautifulSoup(resp.text)
        for i in soup.findAll('div', {'class': 'branch-summary js-branch-row'}):
            yield i.attrs['data-branch-name']

    def get_commits_branch(self):
        for branch in self._get_branches_names():
            commits = []
            resp = requests.get('{}/commits/{}'.format(self.url, branch))
            soup = BeautifulSoup(resp.text)
            for i in soup.find_all('a', {'class': 'message js-navigation-open'}):
               commits.append(i.attrs['title'])
            yield len(commits)

    def get_branches(self):
        return zip(list(self._get_branches_names()),
                   list(self.get_commits_branch()))

    def get_users(self):
        pass


class Repositories:

    def __init__(self):
        self._container = []
    
    def add(self, repository):
        self._container.append(repository)
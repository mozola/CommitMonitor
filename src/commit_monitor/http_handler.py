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
            yield i.text

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
        for i in soup.findAll('a', {'class': 'branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown'}):
            print(f'Branch name: {i.text}')

        for i in soup.findAll('a', {'class': 'branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown'}):
            yield i.text

    def add(self, repository):
        print(repository)
        for branch in self.get_branches(repository.url):
            repo = Repository(repository.name, repository.url)
            repo.branch = branch
            repo.commits = repository.get_commits(branch)
            print(f'Repository branch: {repo.branch}')
            self._container.append(repo)
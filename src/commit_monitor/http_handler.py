import abc
import requests

from bs4 import BeautifulSoup


class IRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_branches(self):
        pass

    @abc.abstractmethod
    def get_commits(self):
        pass

    @abc.abstractmethod
    def get_users(self):
        pass


class Repository(IRepository):

    def __init__(self, name=None, url=None, branch=None):
        self.name = name
        self.url = url
        self.branch = branch
        self.commits: int = None
        self._state = Github()

    def get_commits(self):
        self._state.get_commits()

    def get_branches(self):
        self._state.get_branches()

    def get_users(self):
        self._state.get_users()


class Github(IRepository):

    def _get_branches_names(self, url: str):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text)
        for i in soup.findAll('div', {'class': 'branch-summary js-branch-row'}):
            yield i.attrs['data-branch-name']

    def get_commits(self):
        pass

    def get_branches(self, url):
        return list(self._get_branches_names(url))

    def get_users(self):
        pass


class Gitlab(IRepository):

    def get_commits(self):
        pass

    def get_branches(self):
        pass

    def get_users(self):
        pass

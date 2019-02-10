import abc
import requests

from bs4 import BeautifulSoup


class Commit:

    def __init__(self, url, branch, name):
        self._author = None
        self._date = None
        self._name = name

    def setup_date(self):
        pass

    def setup_name(self):
        pass
    
    def setup_author(self):
        pass

    def add_commit(self, branch):
        pass


class Branch:

    def __init__(self, name, url):
        self._name = name
        self._commits = list(self.setup_commits(url, name))
    

    @property
    def name(self):
        return self._name

    @property
    def commits(self):
        return self._commits

    def setup_name(self):
        pass

    def setup_author(self):
        pass

    def setup_date(self):
        pass

    def setup_commits(self, url, name):
        resp = requests.get('{}/commits/{}'.format(url, name))
        soup = BeautifulSoup(resp.text)
        for i in soup.find_all('a', {'class': 'message js-navigation-open'}):
            yield Commit(name = i.text, branch=name, url=url)


class Repository:

    def __init__(self, name=None, url=None):
        self._name = name
        self._url = url
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
        for i in soup.findAll('a', {'class': 'branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown'}):
            yield Branch(name = i.text, url = self.url)
    '''
    def get_commits(self, branch):
        commit = Commit(self._url)
        return list(commit.add_commit(branch))
    '''

class Repositories:

    def __init__(self):
        self._container = []

    def add(self, repository):
        self._container.append(repository)

    @property
    def container(self):
        return self._container

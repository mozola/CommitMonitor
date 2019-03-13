from enum import Enum
from github import Github

from .branch import Branch


class Repository:

    def __init__(self, token: str):

        self._token = token
        self._name: str = None
        self._auth: str = None
        self._users: list = None
        self._manager: Github = None

    @property
    def is_run(self) -> Github:
        return self._manager is not None

    @property
    def name(self) -> str:
        return self._name

    @property
    def auth(self) -> str:
        return self._auth

    @property
    def branches(self) -> list:
        return [Branch(i) for i in self._manager.get_branches()]

    @property
    def commits(self):
        return self._manager.get_commits()

    @property
    def labels(self):
        labels = self._manager.get_labels()

        if labels not in (None, []):
            return labels

        return None

    @property
    def members(self):
        raise NotImplementedError

    def open(self, organisation: str, project_name: str) -> None:

        repository = Github(self._token)
        self._auth = organisation
        self._name = project_name
        project = f'{organisation}/{project_name}'
        self._manager = repository.get_repo(project)

    def close(self) -> None:
        if not self.is_run:
            raise ConnectionError('Repository is already closed')

        self._manager = None

    def get_open_issues(self) -> list:
        return self._manager.get_issues(state='open')

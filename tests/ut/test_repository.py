import pytest
from src.commit_monitor.repository import Repository

from github.PaginatedList import PaginatedList
from github.GithubException import UnknownObjectException


@pytest.fixture(scope="function")
def repository():
    token = '9bd044ef290694d239a318bef1e605a6fd2c8222'
    repository = Repository(token)
    repository.open('mozola', 'DPW')
    yield repository
    repository.close()


def test_open_close(repository):
    assert repository.is_run


def test_get_repository_name(repository):
    assert repository.is_run
    assert repository.name == 'DPW'


def test_get_repository_auth(repository):
    assert repository.is_run
    assert repository.auth == 'mozola'


def test_get_project_branches(repository):
    assert repository.is_run
    branches = repository.branches
    assert isinstance(branches, PaginatedList)
    assert branches.totalCount == 1


def test_get_project_labels(repository):
    labels = repository.labels
    assert isinstance(labels, PaginatedList)
    assert labels is not None


@pytest.mark.xfail(raises=NotImplementedError)
def test_get_members(repository):
    assert isinstance(repository.members,
                      PaginatedList)


@pytest.mark.xfail(raises=AttributeError)
def test_get_project_opened_tasks(repository):
    assert isinstance(repository.get_open_tasks, PaginatedList)


@pytest.mark.xfail(raises=AttributeError)
def test_get_project_closed_tasks(repository):
    assert isinstance(repository.get_closed_tasks, PaginatedList)


def test_check_name_flow_of_tasks(repository):
    pass


def test_check_name_flow_of_branches(repository):
    pass


@pytest.mark.xfail
def test_get_users_activities():
    return NotImplementedError

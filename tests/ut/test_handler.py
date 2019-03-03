import pytest

from src.commit_monitor.http_handler import Repositories, Commit, Branch


def test_create_commit_object():
    commit = Commit('', '', '')
    assert isinstance(commit, Commit)


def test_create_branch_object():
    pass


def test_create_repository_object():
    pass

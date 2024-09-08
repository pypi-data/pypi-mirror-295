from unittest.mock import Mock

import pytest

from gptcomet.clis.generate.commit import gen_output
from gptcomet.const import COMMIT_OUTPUT_TEMPLATE


@pytest.fixture
def repo():
    return Mock(active_branch=Mock(name="master"))


@pytest.fixture
def commit():
    return Mock(
        hexsha="123456",
        message="test commit message",
        author=Mock(conf_name="John Doe", conf_email="john@example.com"),
    )


def test_gen_output(repo, commit):
    output = gen_output(repo, commit)
    assert output.startswith(
        COMMIT_OUTPUT_TEMPLATE.format(
            author=":construction_worker: [green]John Doe[/]",
            email="[blue]john@example.com[/blue]",
            branch="master",
            commit_hash="123456",
            commit_msg="test commit message",
            git_show_stat="",
        )
    )


def test_gen_output_rich_false(repo, commit):
    output = gen_output(repo, commit, rich=False)
    assert output.startswith(
        COMMIT_OUTPUT_TEMPLATE.format(
            author="John Doe",
            email="john@example.com",
            branch="master",
            commit_hash="123456",
            commit_msg="test commit message",
            git_show_stat="",
        )
    )


def test_gen_output_commit_msg_empty(repo, commit):
    commit.message = ""
    output = gen_output(repo, commit)
    assert output.startswith(
        COMMIT_OUTPUT_TEMPLATE.format(
            author=":construction_worker: [green]John Doe[/]",
            email="[blue]john@example.com[/blue]",
            branch="master",
            commit_hash="123456",
            commit_msg="",
            git_show_stat="",
        )
    )


def test_gen_output_author_email_empty(repo, commit):
    commit.author.conf_name = None
    commit.author.conf_email = None
    output = gen_output(repo, commit)
    assert output.startswith(
        COMMIT_OUTPUT_TEMPLATE.format(
            author="",
            email="",
            branch="master",
            commit_hash="123456",
            commit_msg="test commit message",
            git_show_stat="",
        )
    )


def test_gen_output_repo_none():
    with pytest.raises(AttributeError):
        gen_output(None, Mock())


def test_gen_output_commit_none():
    with pytest.raises(AttributeError):
        gen_output(Mock(), None)

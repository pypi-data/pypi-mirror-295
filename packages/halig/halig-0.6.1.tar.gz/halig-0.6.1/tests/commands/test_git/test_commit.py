import subprocess

import pytest

from halig.commands.git.commit import GitCommitCommand
from halig.settings import Settings


@pytest.fixture
def command(settings: Settings):
    return GitCommitCommand(settings=settings)


def test_repo_is_not_initialized(settings):
    """Given that settings.notebooks_root_path is not a git repo, assert that the command
    initializes the repo upon instantiation"""

    assert not (settings.notebooks_root_path / ".git").is_dir()
    GitCommitCommand(settings=settings)
    assert (settings.notebooks_root_path / ".git").is_dir()


def test_repo_is_initialized(settings):
    """Manually initialize a repo in settings.notebooks_root_path and check that the command instantiation
    is not reinitializing it"""

    p = subprocess.Popen(["git", "init"], cwd=settings.notebooks_root_path)
    p.wait()
    assert (settings.notebooks_root_path / ".git").is_dir()
    GitCommitCommand(settings=settings)
    assert (settings.notebooks_root_path / ".git").is_dir()


def test_run(settings, command, faker):
    """Create a bunch of .age and non-.age files and assert that all .age files are added to git and that the commit
    message is set"""

    for _ in range(10):
        random_file = settings.notebooks_root_path / f"{faker.word()}.txt"
        random_file.touch()

    for _ in range(10):
        random_age_file = settings.notebooks_root_path / f"{faker.word()}.age"
        random_age_file.touch()

    command.run()
    assert settings.notebooks_root_path / ".git" / "index"
    assert settings.notebooks_root_path / ".git" / "index" / "stage"

    assert command.message in command.repo.git.log("--pretty=oneline").splitlines()[0]

    assert "nothing added to commit but untracked files present (use \"git add\" to track)" in command.repo.git.status()
    assert ".age" not in command.repo.git.status()


def test_custom_commit_message(settings, command, faker):
    command.message = faker.word()
    command.run()
    assert command.message in command.repo.git.log("--pretty=oneline").splitlines()[0]

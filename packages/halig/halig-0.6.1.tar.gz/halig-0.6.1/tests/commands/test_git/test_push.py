import shutil

import pytest

from halig.commands.git.commit import GitCommitCommand
from halig.commands.git.push import GitPushCommand


@pytest.fixture
def command(settings, faker):
    """Configure a local remote for testing"""
    commit_command = GitCommitCommand(settings=settings)
    new_path = shutil.copytree(settings.notebooks_root_path, settings.notebooks_root_path / "../remote")
    new_path = new_path.resolve()
    for _ in range(10):
        random_age_file = settings.notebooks_root_path / f"{faker.word()}.age"
        random_age_file.touch()
    commit_command.run()

    push_command = GitPushCommand(settings=settings)

    push_command.repo.create_remote("origin", str(new_path))

    return push_command


def test_push_to_origin(command):
    """Test that the command pushes to the origin remote"""
    command.run()


def test_push_to_custom_remote(settings, command):
    """Test that the command pushes to a custom remote"""

    remote_path = settings.notebooks_root_path / "../remote"
    command.repo.create_remote("custom", str(remote_path.resolve()))
    command.remotes = ["custom"]
    command.run()

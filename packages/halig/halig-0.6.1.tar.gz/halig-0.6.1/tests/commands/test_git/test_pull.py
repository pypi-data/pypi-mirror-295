import shutil

import pytest
from git import Repo

from halig.commands.git.pull import GitPullCommand


@pytest.fixture
def command(settings, faker):
    """Configure a local remote for testing located at settings.notebooks_root_path/../remote, push some .age files to
    that remote
    """
    command = GitPullCommand(settings=settings)

    new_path = shutil.copytree(settings.notebooks_root_path, settings.notebooks_root_path / "../remote")
    new_path = new_path.resolve()

    command.repo.create_remote("origin", str(new_path))

    remote_repo = Repo(new_path)
    for _ in range(10):
        random_age_file = new_path / f"{faker.word()}.age"
        random_age_file.touch()
        remote_repo.index.add([str(random_age_file)])
    remote_repo.index.commit("Update notebooks")

    return command

def test_pull_from_origin(command):
    command.run()

def test_pull_from_custom_origin(settings, command):
    remote_path = settings.notebooks_root_path / "../remote"
    command.repo.create_remote("custom", str(remote_path.resolve()))
    command.remotes = ["custom"]
    command.run()

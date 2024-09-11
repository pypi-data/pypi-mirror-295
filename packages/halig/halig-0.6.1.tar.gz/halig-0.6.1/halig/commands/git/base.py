from pathlib import Path

from git import Repo
from rich import print

from halig.commands.base import BaseCommand
from halig.encryption import Encryptor
from halig.settings import Settings


class GitBaseCommand(BaseCommand):
    @staticmethod
    def __init_repo(repo_path: Path) -> Repo:
        """Check if `repo_path` is a git repo. If not, initialize it"""

        if not (repo_path / ".git").is_dir():
            print(f"[yellow] {repo_path} is not a git repo, initializing ...")
            Repo.init(repo_path)
            return Repo(repo_path)

        return Repo(repo_path)

    def __init__(self, settings: Settings, message: str | None = None):
        super().__init__(settings)
        self.settings = settings
        self.encryptor = Encryptor(self.settings)
        self.message = message or self.settings.default_commit_message
        self.repo = self.__init_repo(self.settings.notebooks_root_path)

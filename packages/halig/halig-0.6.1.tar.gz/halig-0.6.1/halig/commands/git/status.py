from rich import print

from halig.commands.git.base import GitBaseCommand


class GitStatusCommand(GitBaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # pragma: no cover

    def run(self):
        """Show the status of the git repo, including unstaged *.age files"""

        print(self.repo.git.status())  # pragma: no cover

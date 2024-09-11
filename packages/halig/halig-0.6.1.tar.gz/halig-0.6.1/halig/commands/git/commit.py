from halig.commands.git.base import GitBaseCommand


class GitCommitCommand(GitBaseCommand):
    def __init__(self, message: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message or self.settings.default_commit_message

    def run(self):
        """Add all .age files to git and commit them using gitpython"""
        self.repo.index.add(
            [str(path) for path in self.settings.notebooks_root_path.glob("**/*.age")]
        )
        self.repo.index.commit(self.message)

from halig.commands.git.base import GitBaseCommand


class GitPushCommand(GitBaseCommand):
    def __init__(self, remotes: list[str] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remotes = remotes

    def run(self):
        """Push all changes to the remote git repo"""
        if not self.remotes:
            self.repo.remotes.origin.push()
            return

        for remote in self.remotes:
            self.repo.remotes[remote].push()

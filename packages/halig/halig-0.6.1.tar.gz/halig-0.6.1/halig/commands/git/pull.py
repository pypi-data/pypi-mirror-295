from halig.commands.git.base import GitBaseCommand


class GitPullCommand(GitBaseCommand):
    def __init__(
        self, remotes: list[str] | None = None, ref: str | None = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.remotes = remotes
        self.ref = ref

    def run(self):
        """Pull all changes from the remote git repo"""
        if not self.remotes:
            self.repo.remotes.origin.pull(self.ref or "main")
            return

        for remote in self.remotes:
            self.repo.remotes[remote].pull(self.ref or "main")

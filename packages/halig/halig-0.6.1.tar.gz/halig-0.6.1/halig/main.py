#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

from rich import print
from rich.prompt import Prompt
from typer import Argument, Option, Typer

from halig import literals
from halig.__version__ import __version__
from halig.commands.edit import EditCommand
from halig.commands.git.commit import GitCommitCommand
from halig.commands.git.pull import GitPullCommand
from halig.commands.git.push import GitPushCommand
from halig.commands.git.status import GitStatusCommand
from halig.commands.import_unencrypted import ImportCommand
from halig.commands.notebooks import NotebooksCommand
from halig.commands.reencrypt import ReencryptCommand
from halig.commands.search import SearchCommand
from halig.commands.show import ShowCommand
from halig.settings import load_from_file
from halig.utils import capture

git_app = Typer(
    name="git",
    help=literals.GIT_HELP,
    pretty_exceptions_enable=False,
    pretty_exceptions_show_locals=False,
)
app = Typer(
    name="halig", pretty_exceptions_enable=False, pretty_exceptions_show_locals=False
)
app.add_typer(git_app)

config_option = Option(None, "--config", "-c", help=literals.OPTION_CONFIG_HELP)


def complete_note_path(incomplete: str):
    """Build `path = Path(settings.notebooks_root_path / incomplete)`, and complete if:
    - `path` exists:
        - if `path` is a file and ends with `.age`: return it
        - if `path` is a dir: return all its children, non-recursively
    - `path` does not exist: return all occurrences of path.glob("*")
    """
    settings = load_from_file()
    path = settings.notebooks_root_path / incomplete
    if path.exists():
        if path.is_dir():
            for child in path.iterdir():
                yield str(child.relative_to(settings.notebooks_root_path))
        elif path.name.endswith(".age"):
            return str(path.relative_to(settings.notebooks_root_path))
    glob = settings.notebooks_root_path.glob(f"{incomplete}*")
    for path in glob:
        yield str(path.relative_to(settings.notebooks_root_path))


@app.command(help=literals.COMMANDS_NOTEBOOKS_HELP)
@capture
def tree(
    level: int = Option(  # B008
        -1,
        "--level",
        "-l",
        help=literals.OPTION_LEVEL_HELP,
    ),
    include_notes: bool = Option(False, help=literals.OPTION_INCLUDE_NODES_HELP),
    config: Optional[Path] = config_option,  # noqa: UP007
):
    if level < 0:
        level = float("inf")  # type: ignore[assignment]
    settings = load_from_file(config)
    command = NotebooksCommand(
        settings=settings,
        max_depth=level,
        include_notes=include_notes,
    )
    command.run()


@app.command(help=literals.COMMANDS_EDIT_HELP)
@capture
def edit(
    note: Path = Argument(  # noqa: B008
        ...,
        help=literals.ARGUMENT_EDIT_NOTE_HELP,
        autocompletion=complete_note_path,
    ),
    config: Optional[Path] = config_option,  # noqa: UP007
):
    settings = load_from_file(config)
    command = EditCommand(settings=settings, note_path=note)
    command.run()


@app.command(help=literals.COMMANDS_SHOW_HELP)
@capture
def show(
    note: Path = Argument(  # noqa: B008
        ...,
        help=literals.ARGUMENT_SHOW_NOTE_HELP,
        autocompletion=complete_note_path,
    ),
    plain: bool = Option(False, help=literals.OPTION_PLAIN_HELP),  # B008
    config: Optional[Path] = config_option,  # noqa: UP007
):
    settings = load_from_file(config)
    command = ShowCommand(settings=settings, note_path=note, plain=plain)
    command.run()


@app.command(name="import", help=literals.COMMANDS_IMPORT_HELP)
@capture
def import_unencrypted(
    unlink: bool = Option(
        False,
        help=literals.OPTION_UNLINK_HELP,
    ),
    config: Optional[Path] = config_option,  # noqa: UP007
):
    settings = load_from_file(config)
    command = ImportCommand(settings=settings, unlink=unlink)
    files_to_unlink = list(command.get_importables())
    if files_to_unlink:
        if unlink:
            should_unlink = Prompt.ask(
                f"""Unlink flag set, will delete {len(files_to_unlink)} files.
                Have you backed up your data?""",
                choices=["y", "Y", "N", "n"],
            )
            if should_unlink in ["N", "n"]:
                command.unlink = False

        command.run()


@app.command(help=literals.COMMANDS_SEARCH_HELP)
def search(
    term: str,
    index: bool = Option(False, help=literals.OPTION_INDEX_HELP),
    config: Optional[Path] = config_option,  # noqa: UP007
):
    settings = load_from_file(config)
    command = SearchCommand(
        term=term,
        index=index,
        settings=settings,
    )
    command.run()


@app.command(help=literals.COMMANDS_REENCRYPT_HELP)
def reencrypt(config: Path | None = config_option):
    settings = load_from_file(config)
    command = ReencryptCommand(
        settings=settings,
    )
    command.run()


@git_app.command(name="commit", help=literals.COMMANDS_GIT_COMMIT_HELP)
def git_commit(
    message: str | None = None,
    config: Path | None = config_option,
):
    settings = load_from_file(config)
    command = GitCommitCommand(settings=settings, message=message)
    command.run()


@git_app.command(name="push", help=literals.COMMANDS_GIT_PUSH_HELP)
def git_push(
    remotes: list[str] | None = None,
    config: Path | None = config_option,
):
    settings = load_from_file(config)
    command = GitPushCommand(settings=settings, remotes=remotes)
    command.run()


@git_app.command(name="pull", help=literals.COMMANDS_GIT_PULL_HELP)
def git_pull(
    remotes: list[str] | None = None,
    config: Path | None = config_option,
):
    settings = load_from_file(config)
    command = GitPullCommand(settings=settings, remotes=remotes)
    command.run()


@git_app.command(name="status", help=literals.COMMANDS_GIT_STATUS_HELP)
def git_status(
    config: Path | None = config_option,
):
    settings = load_from_file(config)
    command = GitStatusCommand(settings=settings)
    command.run()


@app.command(help=literals.COMMANDS_VERSION)
@capture
def version():
    print(__version__)


if __name__ == "__main__":
    app()

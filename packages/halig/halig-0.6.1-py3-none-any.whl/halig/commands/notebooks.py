from collections import deque
from pathlib import Path

from rich import print
from rich.tree import Tree

from halig.commands.base import BaseCommand


class NotebooksCommand(BaseCommand):
    def __init__(
        self,
        max_depth: int | float,
        include_notes: bool = False,
        *args,
        **kwargs,
    ):
        self.max_depth = max_depth
        self.include_notes = include_notes
        super().__init__(*args, **kwargs)

    def build_tree(self, root_path: Path):
        tree = Tree(root_path.name)
        q: deque[tuple[Path, Tree, int | float]] = deque([(root_path, tree, 0)])
        while q:
            current_folder_path, current_tree_node, depth = q.popleft()
            if depth >= self.max_depth:
                break
            for item in sorted(current_folder_path.iterdir()):
                if item.is_dir():
                    if item.name != ".git":
                        item_tree_node = current_tree_node.add(item.name)
                        q.append((item, item_tree_node, depth + 1))
                elif self.include_notes and item.name.endswith(".age"):
                    current_tree_node.add(item.name)
        return tree

    def run(self):
        print(self.build_tree(self.settings.notebooks_root_path))  # pragma: no cover

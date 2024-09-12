import os

import pyperclip  # type: ignore

from llm_code_context.config_manager import ConfigManager
from llm_code_context.file_selector import FileSelector


class FolderStructureDiagram:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def generate_tree(self, file_paths: list[str]) -> str:
        sorted_paths = sorted(self._make_relative(path) for path in file_paths)
        tree_dict = self._build_tree_structure(sorted_paths)
        return self._format_tree({os.path.basename(self.root_dir): tree_dict})

    def _make_relative(self, path: str) -> str:
        return os.path.relpath(path, self.root_dir)

    def _build_tree_structure(self, paths: list[str]) -> dict:
        root: dict = {}
        for path in paths:
            current = root
            for part in path.split(os.sep):
                current = current.setdefault(part, {})
        return root

    def _format_tree(self, tree: dict, prefix: str = "") -> str:
        lines = []
        items = list(tree.items())
        for i, (name, subtree) in enumerate(items):
            is_last = i == len(items) - 1
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{name}")
            if subtree:
                extension = "    " if is_last else "│   "
                lines.append(self._format_tree(subtree, prefix + extension))
        return "\n".join(lines)


def get_fs_diagram():
    project_root = ConfigManager.create_default().project_root()
    file_paths = FileSelector.create([".git"]).get_all()
    return FolderStructureDiagram(project_root).generate_tree(file_paths)


def main():
    pyperclip.copy(get_fs_diagram())


if __name__ == "__main__":
    main()

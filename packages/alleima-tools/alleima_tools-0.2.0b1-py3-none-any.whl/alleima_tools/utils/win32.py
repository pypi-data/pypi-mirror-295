from pathlib import Path

from pydantic import BaseModel, RootModel
from win32com.client import Dispatch


class Shortcut(BaseModel):
    """Shortcut file information."""

    path: Path
    target: Path | None = None

    @classmethod
    def from_path(cls, path: Path | str) -> "Shortcut":
        """Create a Shortcut instance from a path.

        Args:
            path (Path): Path to the shortcut file.

        Returns:
            Shortcut instance.
        """
        if isinstance(path, str):
            path = Path(path)
        return cls(path=path, target=get_shortcut_target(path))


class Shortcuts(RootModel):
    root: list[Shortcut]

    @classmethod
    def from_folder(cls, folder_path: Path | str) -> "Shortcuts":
        """Create a Shortcuts instance from a folder path.

        Args:
            folder_path (Path): Path to the folder containing the shortcut files.

        Returns:
            Shortcuts instance.
        """
        if isinstance(folder_path, str):
            folder_path = Path(folder_path)
        return cls(
            root=[
                Shortcut.from_path(file)
                for file in folder_path.iterdir()
                if file.suffix == ".lnk"
            ]
        )

    def __getitem__(self, index: int) -> Shortcut:
        return self.root[index]

    def __iter__(self):
        return iter(self.root)


def get_shortcut_target(path: Path | str) -> Path:
    """Get the target of a Windows shortcut file.

    Args:
        path (Path): Path to the shortcut file.

    Returns:
        Target of the shortcut file.
    """
    if isinstance(path, str):
        path = Path(path)
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(path))
    return Path(shortcut.Targetpath)


if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table

    table = Table(title="Shortcut Files")

    table.add_column("Shortcut File", style="cyan")
    table.add_column("Target File", style="magenta", no_wrap=True)

    parent_folder_path = Path("G:/Engineering")
    search_folder_path = parent_folder_path / "HTML Space" / "Stores Dwgs"

    shortcuts = Shortcuts.from_folder(folder_path=search_folder_path)
    for shortcut in shortcuts:
        if shortcut.target.suffix == ".pdf" and "M04" in shortcut.target.stem:
            table.add_row(
                f"{shortcut.path.stem}",
                f"[link={shortcut.target.as_uri()}]{shortcut.target.relative_to(parent_folder_path)}[/link]",
            )

    console = Console()

    console.print(table)

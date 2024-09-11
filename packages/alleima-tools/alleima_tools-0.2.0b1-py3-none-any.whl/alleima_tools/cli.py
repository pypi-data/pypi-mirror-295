# ruff: noqa: UP007
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

from alleima_tools.cli_helpers.versions import generate_build_number

app = typer.Typer()


@app.command()
def build_number():
    """Generate a build number based on the current date and time.

    The first 8 characters of the build number are the current date in the format
    'YYYYMMDD'. The last 3 characters ara counter of 2 minute intervals since midnight.

    Examples:

        >>> generate_build_number()

        '20220131120'
    """
    print(generate_build_number())


@app.command()
def shortcuts(
    folder_path: Annotated[Path, typer.Argument(help="Path to the folder to search.")],
    target_extension: Annotated[
        Optional[str],
        typer.Option(help="Target file extension without the dot."),
    ] = "pdf",
    name_filter: Annotated[
        Optional[str], typer.Option(help="Filter the target file name.")
    ] = None,
):
    """Print a linked table of the targets of Windows shortcuts in a folder."""
    from rich.console import Console
    from rich.table import Table

    from alleima_tools.utils.win32 import Shortcuts

    table = Table(title="Shortcut Files")

    table.add_column("Shortcut File", style="cyan")
    table.add_column("Target File", style="magenta", no_wrap=True)

    shortcuts = Shortcuts.from_folder(folder_path=folder_path)
    for shortcut in shortcuts:
        if shortcut.target.suffix == f".{target_extension}":
            if name_filter is not None and name_filter not in shortcut.target.stem:
                continue

            table.add_row(
                f"{shortcut.path.stem}",
                f"[link={shortcut.target.as_uri()}]{shortcut.target!s:.100}[/link]",
            )

    console = Console()

    console.print(table)


if __name__ == "__main__":
    app()

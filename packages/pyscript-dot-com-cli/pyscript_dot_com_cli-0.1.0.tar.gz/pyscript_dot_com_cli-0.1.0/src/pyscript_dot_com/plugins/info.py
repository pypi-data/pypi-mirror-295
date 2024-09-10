from pyscript import app, plugins
from pyscript_dot_com import cli

import typer


@app.command()
def info(
    metadata: bool = typer.Option(
        True, "--metadata", help="Display metadata information about the project"
    ),
    files: bool = typer.Option(False, "--files", help="Display all project files"),
):
    """
    Show information of the current project.
    """

    if metadata:
        cli.show_project_metadata()
    if files:
        cli.show_project_files_info()


@plugins.register
def pyscript_subcommand():
    return info

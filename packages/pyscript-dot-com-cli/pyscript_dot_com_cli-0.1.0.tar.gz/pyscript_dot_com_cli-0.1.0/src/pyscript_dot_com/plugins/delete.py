import typer

from pyscript import app, console, plugins
from pyscript.cli import Abort
from pyscript_dot_com import cli
from pyscript_dot_com.utils import is_uuid


@app.command()
def delete(
    project_slug_or_id: str = typer.Argument(
        None, help="Delete a project by passing in the project ID or slug."
    ),
    delete_all: bool = typer.Option(False, "--all", help="Delete all user projects."),
    confirmed: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation prompt and delete the project.",
    ),
):
    """
    Delete the current project if inside a project folder.
    Can also delete a project by its ID or slug.
    Can also delete all projects via `--all`.
    """
    if (project_slug_or_id is not None) and delete_all:
        raise Abort(
            "--all should be used standalone i.e. without supplying a project identifer (slug/id)"
        )
    if delete_all:
        if confirmed:
            console.print("Auto confirmation is not allowed with --all flag.")
        typer.confirm("Are you sure you want to delete all projects?", abort=True)
    else:
        if confirmed:
            console.print("Auto confirmed the deletion of the project.")
        else:
            typer.confirm("Are you sure you want to delete this project?", abort=True)

    if project_slug_or_id:
        if is_uuid(project_slug_or_id):
            cli.delete_project_by_id(project_slug_or_id)
        else:
            cli.delete_project_by_slug(project_slug_or_id)
    elif delete_all:
        cli.delete_all_projects()
    else:
        cli.delete_project()


@plugins.register
def pyscript_subcommand():
    return delete

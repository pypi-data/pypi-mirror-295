import typer

from pyscript import app
from pyscript.cli import Abort
from pyscript_dot_com import cli

versions_app = typer.Typer()
app.add_typer(
    versions_app, name="version", help="Manage project versions.", no_args_is_help=True
)


@versions_app.command("create")
def version_create():
    """
    Create a version to make a snapshot of the current state of
    your project. Versions can be viewed, but cannot be edited.
    """
    cli.create_version()


@versions_app.command("delete")
def version_delete(
    version: str = typer.Argument(None, help="Version number to be deleted.")
):
    """
    Delete the provided version number from the project.
    """
    if version:
        cli.delete_version(version)
    else:
        raise Abort("Please specify a version to delete")


@versions_app.command("info")
def version_info(
    version: str = typer.Argument(None, help="Version number to be displayed.")
):
    """
    Display the information related to the provided version number.
    """
    if version:
        cli.get_version(version)
    else:
        raise Abort("Please specify a version.")


@versions_app.command("list")
def version_list():
    """
    List all the versions of the project.
    """
    cli.show_project_versions()

import typer

from pyscript import app, plugins
from pyscript.cli import Abort
from pyscript_dot_com import cli
from pyscript_dot_com.utils import (
    PROJECT_IDENTIFIER_HELPER,
    is_uuid,
    parse_project_identifier,
)


@app.command()
def copy(
    project_identifier: str = typer.Argument(
        None, help=f"Identifier for a project. {PROJECT_IDENTIFIER_HELPER}"
    ),
    new_name: str = typer.Argument(
        None,
        help="New name of the project. If not supplied, `copy` will be suffixed "
        "to the original name. (e.g: `Corner Detection copy`)",
    ),
    download: bool = typer.Option(
        False,
        "--download",
        help="Download files along with copying the project into the PyScript.com account. "
        "Disabled by default.",
    ),
    confirmed: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation prompt and copy the project.",
    ),
):
    """
    Copy the project. Project can be either be identified using the project ID
    or the combination of username and project slug.
    """
    if not project_identifier:
        if download:
            raise Abort("Already inside the project folder, cannot download.")
        cli.copy_from_inside_project(None, new_name)
    else:
        try:
            username, project_slug, project_id = parse_project_identifier(
                project_identifier
            )
        except ValueError as e:
            raise Abort(e)

        if is_uuid(project_identifier):
            project_id = project_identifier
            cli.copy_project_by_id(project_id, new_name, download, confirmed)
        elif username and project_slug:
            cli.copy_project_by_username_and_slug(
                username, project_slug, new_name, download, confirmed
            )
        # If we only have a single identifier, we will assume that it is the project slug
        else:
            cli.copy_project_by_username_and_slug(
                None, project_slug, new_name, download, confirmed
            )

        # if len(identifier) == 2:
        #     username, project_slug = identifier
        #     cli.copy_project_by_username_and_slug(
        #         username, project_slug, new_name, download
        #     )
        # else:
        #     project_id = identifier
        #     cli.copy_project_by_id(project_id, new_name, download)


@plugins.register
def pyscript_subcommand():
    return copy

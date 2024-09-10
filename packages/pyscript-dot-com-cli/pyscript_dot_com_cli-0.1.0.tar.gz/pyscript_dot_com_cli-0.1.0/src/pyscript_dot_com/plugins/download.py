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
def download(
    project_identifier: str = typer.Argument(
        None, help=f"Identifier for a project. {PROJECT_IDENTIFIER_HELPER}"
    ),
    confirmed: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation prompt and download the project.",
    ),
):
    """
    Download the project. Project can be either be identified using the project ID,
    project slug (if the project is owned by the current user), the the combination
    of username and project slug in the following format: @USERNAME/SLUG,
    eg: @fpliger/location-api or the project url,
    eg: https://username.pyscriptapps.com/project-slug
    """

    if not project_identifier:
        cli.download_project_updates(confirmed)
    else:
        try:
            username, project_slug, project_id = parse_project_identifier(
                project_identifier
            )
        except ValueError as e:
            raise Abort(e)

        if is_uuid(project_identifier):
            project_id = project_identifier
            cli.download_project_by_id(project_id, confirmed)
        elif username and project_slug:
            cli.download_project_by_user_and_slug(username, project_slug, confirmed)
        # If we only have a single identifier, we will assume that it is the project slug
        else:
            cli.download_project_by_user_and_slug(None, project_slug, confirmed)


@plugins.register
def pyscript_subcommand():
    return download

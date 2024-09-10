import typer

from pyscript import app, plugins
from pyscript_dot_com import cli


@app.command()
def upload(
    as_archive: bool = typer.Option(
        False,
        "-a",
        "--archive",
        help=(
            "Upload archive of the whole project (rather than the default: "
            "individual files) to the API."
        ),
    ),
    confirmed: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation prompt and upload the project.",
    ),
):
    """
    Upload the current project.
    """
    manifest = cli.get_dot_com_manifest()
    project_id = manifest.get("project_id") if manifest is not None else None

    if project_id is None:
        # will also upload it
        cli.register_project()
    else:
        cli.upload_project(as_archive=as_archive, confirmed=confirmed)


@plugins.register
def pyscript_subcommand():
    return upload

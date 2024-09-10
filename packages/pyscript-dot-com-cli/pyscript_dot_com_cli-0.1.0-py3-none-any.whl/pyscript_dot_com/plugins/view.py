from typing import Optional

import typer
from typing_extensions import Annotated

from pyscript import app, plugins
from pyscript_dot_com import cli


@app.command(name="view")
def view(
    version: Annotated[Optional[str], typer.Argument()] = None,
):
    """
    View the current project in a browser.
    """

    cli.view_project(version)


@plugins.register
def pyscript_subcommand():
    return view

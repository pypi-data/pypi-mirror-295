from pyscript.cli import Abort
from pyscript import app, plugins
from pyscript_dot_com import cli

import typer


# Suffix on the function name to avoid clash with built-in 'list'.
@app.command("list")
def list_(
    username: str = typer.Option(
        "",
        "--username",
        help="List projects for a particular user by passing --username. "
        "Not supplying is equivalent to using your own username.",
    ),
    search: str = typer.Option(
        "",
        "--search",
        "-s",
        help="List projects matching some search criteria. "
        "These are searched across all public projects.",
    ),
):
    """
    List projects associated with a particular user or matching a certain criteria.
    The output is sorted by project slug.
    """
    if username and search:
        raise Abort("Only one of --username OR --search should be used.")

    cli.list_projects(username=username, search=search)


@plugins.register
def pyscript_subcommand():
    return list_

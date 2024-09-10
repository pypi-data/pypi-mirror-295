import typer

from pyscript import app, plugins
from pyscript_dot_com import cli


@app.command()
def login(
    api_key: str = typer.Option(
        "",
        "--api_key",
        "-k",
        help="Login via API key.",
    ),
):
    """
    Login to pyscript.com, use `--api_key` to login via API key.
    By default it will open a browser window to login via the web interface.
    """
    cli.login(api_key=api_key)


@plugins.register
def pyscript_subcommand():
    return login

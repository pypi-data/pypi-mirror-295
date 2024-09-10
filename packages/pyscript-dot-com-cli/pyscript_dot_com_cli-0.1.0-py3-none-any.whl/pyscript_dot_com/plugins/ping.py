from pyscript import app, plugins
from pyscript_dot_com import cli


@app.command()
def ping():
    """
    Ping the API to ensure settings / authentication.
    """
    cli.ping()


@plugins.register
def pyscript_subcommand():
    return ping

from pyscript import app, plugins
from pyscript_dot_com import cli


@app.command()
def logout():
    """
    Logout of pyscript.com.
    """
    cli.logout()


@plugins.register
def pyscript_subcommand():
    return logout

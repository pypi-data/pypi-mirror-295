from pyscript import app, plugins
from pyscript_dot_com.config import settings
from pyscript_dot_com.renderers import display_config


@app.command()
def config():
    """
    Display your settings.
    """
    display_config(settings)


@plugins.register
def pyscript_subcommand():
    return config

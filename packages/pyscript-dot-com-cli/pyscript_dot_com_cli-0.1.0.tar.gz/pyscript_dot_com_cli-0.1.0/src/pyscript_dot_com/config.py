# PyScript.com configs
import os
from pathlib import Path

import platformdirs
from pydantic import BaseSettings

APP_AUTHOR = "Anaconda, Inc"
APP_NAME = "pyscript.com"
CONFIG_FILENAME = ".env"
IGNORE_FILENAME = ".ignore"

DATA_DIR = Path(platformdirs.user_data_dir(appname=APP_NAME, appauthor=APP_AUTHOR))
LOCAL_CONFIG_DIR = Path(f".{APP_NAME}")
GLOBAL_ENV_FILE = DATA_DIR / CONFIG_FILENAME
LOCAL_ENV_FILE = LOCAL_CONFIG_DIR / CONFIG_FILENAME
GLOBAL_IGNORE_FILE = DATA_DIR / IGNORE_FILENAME
LOCAL_IGNORE_FILE = LOCAL_CONFIG_DIR / IGNORE_FILENAME

IAM_LOGIN_PREFIX = "/self-service/login/api"


class Settings(BaseSettings):
    # These are the production settings. Use your own .env file for local development
    # and when working the with dev (aka. staging) server.
    #
    # Local:
    # API_HOST="http://localhost:8000"
    # API_PREFIX=""
    #
    # Dev:
    # API_HOST="https://pyscript-dev.com"
    #
    api_host = "https://pyscript.com"
    api_base = "/api"
    api_prefix = f"{api_base}/projects"

    # File patterns to ignore when uploading projects to the API.
    ignore = set()

    # The default name of a project's compressed file archive.
    archive_name = "archive"

    # The archive format for compressing the project.
    archive_format = "zip"

    # File patterns to ignore when creating archives to upload to the API.
    archive_ignore = {
        ".*",  # dot files.
        "*.pyc",  # Python compiled bytecode.
    }

    # Where we keep the pyscript.com manifest for registered projects.
    @property
    def hidden_directory(self):
        # The split gives, e.g. ["https", "pyscript.com"].
        return "." + self.api_host.split("://")[1]

    @property
    def manifest_path(self):
        return os.path.join(self.hidden_directory, "manifest.json")

    # ?
    _sources = []

    class Config:
        # `str(LOCAL_ENV_FILE)` takes priority over `str(GLOBAL_ENV_FILE)`
        env_file = str(GLOBAL_ENV_FILE), str(LOCAL_ENV_FILE)

    def __init__(self, global_ignore_path=None, local_ignore_path=None, *args, **kws):
        super().__init__(*args, **kws)

        for path in (global_ignore_path, local_ignore_path):
            if path:
                self.load_ignore(path)
                self._sources.append(path)

    def load_ignore(self, ignore_file_path):
        """
        Load files to ignore from `ignore_file_path` into self.ignore

        Inputs:

            - ignore_file_path (str|Path): path to file to read values from
        """

        ignore_file_path = Path(ignore_file_path)
        if ignore_file_path.exists():
            with ignore_file_path.open() as ignore_file:
                files_to_ignore = {
                    val
                    for val in ignore_file.read().split("\n")
                    if val and not val.startswith("#")
                }

                self.ignore.update(files_to_ignore)


settings = Settings(DATA_DIR / IGNORE_FILENAME, LOCAL_CONFIG_DIR / IGNORE_FILENAME)

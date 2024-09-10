"""Functions to interact with the PyScript Projects service."""

from typing import BinaryIO, Optional
from urllib.parse import urlencode

import requests

from pyscript.cli import Abort

from . import auth
from .config import settings


def ping():
    """
    Ping the API to confirm settings / authentication.
    """
    response = _call("get", "/healthz", authorized=False)
    return response.json()


# Users #############################################################################


def get_current_user_details():
    """
    Get details of currently logged in user.
    """
    auth.set_prefix("/api/auth")

    response = _call("get", "/whoami")

    auth.set_prefix(settings.api_prefix)

    return response.json()


# Projects #############################################################################


def delete_project(project_id):
    """
    Delete a project.
    """
    response = _call("delete", f"/{project_id}")
    if response.status_code != 200:
        raise Abort("Error deleting the project.")

    return True


def copy_project(project_id, new_name):
    """
    Copy a project.
    """
    response = _call("post", f"/{project_id}/forks", payload={"name": new_name})
    if response.status_code != 200:
        raise Abort("Error copying the project.")

    return response.json()


def get_project(project_id: str):
    """
    Get a project's metadata.
    """
    response = _call("get", f"/{project_id}")
    return response.json()


def get_project_by_user_and_slug(username: Optional[str], project_slug: str):
    """
    Get a project by username if present and slug
    """
    if not username:
        user_details = get_current_user_details()
        if user_details["username"]:
            username = user_details["username"]
        else:
            username = user_details["id"]

    response = _call("get", f"/{username}/{project_slug}")
    if response.status_code == 404:
        raise Abort(
            f"Project with slug {project_slug} doesn't exist for user {username}"
        )
    return response.json()


def list_projects(username: Optional[str] = None, search: Optional[str] = None):
    """
    List projects.
    """
    params = {}

    if username:
        params["user"] = username
        params["scope"] = "other"

    if search:
        params["search"] = search
        params["scope"] = "other"

    response = _call("get", "/", params=params)
    # page_size is 0, so we get all results at once.
    return response.json()["results"]


# Versions #############################################################################


def create_version(project_id: str):
    """
    Create a versioned snapshot of a project.
    """

    endpoint = f"/{project_id}/versions"
    payload = {
        "index_file": "index.html",
        "project_id": project_id,
        "status": "published",
    }
    response = _call(
        "post",
        endpoint,
        payload=payload,
    )
    return response.json()


def delete_version(project_id: str, version: str):
    """
    Delete the referenced version.
    """
    endpoint = f"/{project_id}/versions/{version}"
    response = _call("delete", endpoint)
    if response.status_code == 404:
        raise Abort(f"Version {version} not found")


def get_version(project_id: str, version: str):
    """
    Get information from the API about the referenced version.
    """
    endpoint = f"/{project_id}/versions/{version}"
    response = _call("get", endpoint)
    if response.status_code == 404:
        raise Abort(f"Version {version} not found")
    return response.json()


def list_versions(project_id: str):
    """
    List the versions of a project.
    """
    endpoint = f"/{project_id}/versions"
    response = _call("get", endpoint)
    return response.json()["results"]


def publish_version(project_id: str, version: str):
    """
    Publish a version.
    """
    endpoint = f"/{project_id}/versions/{version}"
    response = _call("put", endpoint, payload={"published": True})

    return response.json()


def register_project(type: str, name: str, description: str = ""):
    """
    Register a project.
    """

    endpoint = "/"

    response = _call(
        "post",
        endpoint,
        payload={
            "type": type,
            "name": name,
            "description": description,
            "register_only": True,
        },
    )

    return response.json()


def unpublish_version(project_id: str, version: str):
    """
    Publish a version.
    """
    endpoint = f"/{project_id}/versions/{version}"
    response = _call("put", endpoint, payload={"published": False})

    return response.json()


# Files ################################################################################


def delete_file(project_id: str, filepath: str):
    """
    Delete a file from the latest version of a project.
    """
    endpoint = f"/{project_id}/files"
    encoded = urlencode({"file_path": filepath})
    response = _call("delete", f"{endpoint}?{encoded}")
    return response.json()


def download_file(url, filepath=None):
    """
    Download a file at url into the specified filename. If filename is None
    downloads it to <current directory>/<filename on url>

    Inputs:
        - url (string): url to file
        - filepath (Optional, string): path where the downloaded file will be saved
    """
    if not filepath:
        filepath = url.split("/")[-1]

    # Let's make sure the parent path of filepath exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)

    return filepath


def list_files(project_id: str, ignore_empty_directories: bool = True):
    """
    List the files in the latest version of a project.
    """
    endpoint = f"/{project_id}/files"
    response = _call("get", endpoint)
    result = response.json()

    if ignore_empty_directories:
        result = [
            file_metadata
            for file_metadata in result
            if not file_metadata["path"].endswith("/")
        ]

    return result


def upload_archive(project_id: str, archive_to_upload: BinaryIO):
    """
    Upload an archive to the latest version of a project.
    """
    endpoint = f"/{project_id}/files"
    response = _call(
        "post",
        endpoint,
        params={"archive": True},
        files={"file": archive_to_upload},
    )
    return response.json()


def upload_file(project_id: str, file_to_upload: BinaryIO, override: bool = False):
    """
    List the files in the latest version of a project.
    """

    method = "post" if not override else "put"

    endpoint = f"/{project_id}/files"
    response = _call(
        method, endpoint, files={"file": (file_to_upload.name, file_to_upload)}
    )
    return response.json()


# Helpers ##############################################################################


def _call(method, path, params=None, payload=None, files=None, authorized=True):
    """
    Wraps calling the API.
    Will always exit with a helpful error message if anything goes wrong (a non
    2xx response status).
    The payload is a Python object that's JSON serializable.
    """
    method = method.lower()
    hostname = auth.get_hostname()
    prefix = auth.get_prefix()
    url = f"{hostname}{prefix}{path}"

    kws = dict()

    api_key = auth.get_api_key()
    if api_key:
        kws["headers"] = {"Authorization": f"Bearer {api_key}"}
    else:
        token = auth.get_credentials()
        if token:
            kws["cookies"] = token

    if params:
        kws["params"] = params

    if method in ("post", "put"):
        if payload:
            kws["json"] = payload

        if files:
            kws["files"] = files

    response = getattr(requests, method)(url, **kws)

    if response.ok:
        return response

    else:
        if response.status_code in [401, 403]:
            message = (
                "Unable to retrieve the necessary information from "
                "pyscript.com.\nPlease check that you are logged in or "
                "your session is still valid. Run 'pyscript login' to "
                "log in again or reach out to us if you require help."
            )
        elif response.status_code == 404:
            message = (
                "Unable to find the the requested resource.\nPlease "
                "check the details and try again. If the problem "
                "persists, try to logging in again with 'pyscript login'. "
                "If you require further assistance, please reach out to us."
            )
        elif response.status_code == 409:
            message = (
                "Unable to complete the request, it's likely that a project "
                "already exists with the same name. Please check the details "
                "and try again."
            )
        else:
            message = (
                "Unable to complete the request.\nPlease check the "
                "details and try again. If the problem persists, try "
                "to logging in again with 'pyscript login'. If you require "
                "further assistance, please reach out to us."
            )

        raise Abort(message)

        # TODO: response.text here needs to be better handled. Adding to help
        #       debugging for now.
        # raise Abort(
        #     f"There was a problem connecting to {url}:\n\n"
        #     + f"{response.status_code} {response.reason}\n\n"
        #     + f"{response.text}"
        # )

import datetime
import json
import os
import shutil
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional, Union

import toml
from rich.progress import track
from rich.prompt import Prompt

from pyscript import config as core_config
from pyscript import console, typer
from pyscript.cli import Abort, ok

from . import auth, renderers, service
from .config import settings
from .utils import calculate_s3_etag

# PyScript OSS project config ##########################################################


def get_pyscript_project_config_file_path() -> Path:
    """Return the path to the pyscript project config file in the current directory.

    Return None if no such config file exists.

    The project config file can either be toml or json.

    e.g. pyscript.toml or pyscript.json

    """

    # e.g. 'pyscript.toml'
    project_config_basename = os.path.basename(core_config["project_config_filename"])

    # e.g. 'pyscript'
    project_config_prefix, _ = os.path.splitext(project_config_basename)

    for config_language in ["toml", "json"]:
        config_file_path = Path(f"{project_config_prefix}.{config_language}")
        if config_file_path.exists():
            break

    else:
        config_file_path = None

    return config_file_path


def get_pyscript_project_config() -> Union[dict, None]:
    """Return the pyscript project config.

    Return None if no pyscript project config file exists.

    """

    project_config_file_path = get_pyscript_project_config_file_path()
    if project_config_file_path is None:
        return None

    language_module = json if project_config_file_path.suffix == ".json" else toml

    with open(project_config_file_path, "r") as f:
        config = language_module.load(f)

    return config


def requires_pyscript_project_config(func):
    """
    Decorator to ensure a command is run in a project that has a pyscript config
    file (either pyscript.toml or pyscript.json).

    """

    def inner(*args, **kwargs):
        project_config = get_pyscript_project_config()
        if project_config is None:
            # Get current directory
            current_directory = Path.cwd()
            wants_to_create = typer.confirm(
                "No project configuration file found at the current location("
                f"'{current_directory}'), but is required for this command.\n"
                "Would you like to create one?"
            )
            if not wants_to_create:
                raise Abort(
                    "Cannot find a project config file (pyscript.toml or pyscript.json) "
                    "in the current directory.\n"
                    "Please [bold]change into the project's directory[/bold] "
                    "for this command to work."
                )

            project_config = create_project_configuration()

        return func(project_config, *args, **kwargs)

    return inner


# pyscript.com manifest ################################################################


def delete_dot_com_hidden_directory() -> dict:
    """Deletes the contents of the .pyscript.com hidden directory.

    Returns True if the directory was deleted successfully, otherwise False.

    """

    hidden_directory_path = Path(settings.hidden_directory)
    if not hidden_directory_path.is_dir():
        return False

    shutil.rmtree(hidden_directory_path)

    # if hidden_directory_path exists, then we are in the root of our project directory
    console.print(
        "Project deleted from pyscript.com and the local folder has been unlinked.\n"
        f"To delete local files, run `rm -r {Path.cwd().name}` "
        "from the parent directory.",
        style="bold green",
    )

    return True


def get_dot_com_manifest_path(project_path: Path = None) -> Path:
    """Returns the path to the pyscript.com manifest, using project_path as parent.

    If not supplied, the current working directory is used."""
    project_path = project_path or Path.cwd()
    return project_path / settings.manifest_path


def get_dot_com_manifest() -> dict:
    """Returns the contents of the pyscript.com manifest.

    Returns None if no manifest file exists.

    """

    manifest_path = get_dot_com_manifest_path()
    if not manifest_path.is_file():
        return None

    with manifest_path.open("r") as f:
        manifest = json.load(f)

    return manifest


def write_dot_com_manifest(project_path=None, **kwargs):
    """
    Create/update the pyscript.com manifest.
    """

    manifest_path = get_dot_com_manifest_path(project_path)

    if manifest_path.is_file():
        manifest = get_dot_com_manifest()

    else:
        manifest = dict()

    manifest.update(kwargs)
    manifest_path.parent.mkdir(exist_ok=True)

    # Writes the manifest.json file to the hidden .pyscript.com directory
    # and saves the project info to the manifest.
    # The project info is used to identify the project when uploading files,
    # mapping the local files to the remote project.
    with manifest_path.open("w") as f:
        json.dump(manifest, f, indent=2)


def requires_dot_com_project_id(func):
    """
    Decorator to ensure a command is run in a project that has been registered on
    pyscript.com, passing in just the project id.

    """

    def inner(*args, **kwargs):
        manifest = get_dot_com_manifest()
        if manifest is None:
            raise Abort(
                "You must upload your project to pyscript.com before this command will work.\n"
                "Please type: pyscript upload\n"
                "Alternatively, you may need to provide extra arguments to this command, please "
                "use --help to see the required arguments."
            )

        project_id = manifest.get("project_id")
        if project_id is None:
            raise Abort(
                "No project id in the manifest. You must upload your project to pyscript.com "
                "before this command will work. Please type: pyscript upload"
            )

        return func(project_id, *args, **kwargs)

    return inner


def requires_dot_com_manifest(func):
    """
    Decorator to ensure a command is run in a project that has been registered on
    pyscript.com, passing in the entire pyscript.com manifest.

    """

    def inner(*args, **kwargs):
        manifest = get_dot_com_manifest()
        if manifest is None:
            raise Abort(
                "You must register and upload your project with the API before this "
                "command will work. Please type: pyscript upload"
            )
        return func(manifest, *args, **kwargs)

    return inner


def setup_cli(welcome_msg: str):
    """
    Take the user through a walkthrough to get their CLI setup with PyScript.com.

    """

    hostname = settings.api_host

    console.print(welcome_msg, style="bold green")

    has_account = typer.confirm(
        "Let's get your CLI setup with Pyscript.com, do you already have an account?"
    )

    if not has_account:
        console.print("Opening your web browser for you to create an account.")
        webbrowser.open_new_tab(f"{hostname}/registration")
        Prompt.ask(
            "Press enter when you have created an account, to continue with your CLI setup."
        )

    has_api_key = typer.confirm(
        "The preferred way to authenticate is using an API key. Do you have one?"
    )
    if has_api_key:
        api_key = Prompt.ask("Please enter your API key:", password=True)
        login("You are all set, go and make history!", api_key)
    else:
        wants_to_create = typer.confirm("Okay, would you like to create one?")
        if wants_to_create:
            console.print(
                "Great! We just need to open your web browser again, so "
                "you can login and we will do the rest!"
            )
            auth.login()
            api_key = auth.create_and_save_api_key()
            console.log(
                "Your API key has been created and saved, you can find "
                "it in your PyScript.com account with the name 'PyScript-cli'."
            )
        else:
            console.print(
                "No problem, you can always create one later, if you "
                "change your mind. Opening your browser for you to login."
            )
            login("You are all set, go and make history!")

    ok("You are all set, go and make history!")


def login(welcome_msg="Welcome back to PyScript.com!", api_key: str = ""):
    """
    Go through the process of logging the user into the API host.

    1) Create a unique id that identifies the user's login 'flow'.
    2) Start a local webserver that the user can be redirected to at the end of the
       authentication dance.
    3) Open a webbrowser at '<auth server>/api/auth/login' passing the flow id and the
       local webserver port as a query parameter.
    4) The user does the OIDC login dance :)
    5) When the user has logged in, they are redirected to the local webserver.
    6) Call the auth server with the flow id to retrieve the user's auth token (a JWT)
       and store it in their local keyring.
    """

    if not api_key:
        console.print("Your web browser has been opened for you to login.")
        try:
            token = auth.login()

        except Exception:  # NOQA
            raise Abort("Error completing the login process. Please try again.")

        if token is None:
            raise Abort("Could not complete logging you in. Please try again.")
    else:
        auth.set_api_key(api_key)

    ok(welcome_msg)


def logout():
    """
    Clear the user's token.
    """
    auth.logout()
    ok("See you soon!")


def ping():
    """
    Ping the API to confirm connection to the service.
    """
    answer = service.ping()
    if answer == "ok":
        ok("Pong.")

    else:
        raise Abort("Cannot connect.")


def list_projects(username: Optional[str] = None, search: Optional[str] = None):
    """
    List the current user's projects.
    """

    projects = service.list_projects(username, search)
    sorted_projects = sorted(projects, key=lambda p: p["slug"])
    for_display = []
    keys = ["slug", "name", "id"]
    for project in sorted_projects:
        for_display.append({f"project_{key}": project[key] for key in keys})

    renderers.display_projects(for_display)
    suffix = "" if len(sorted_projects) == 1 else "s"
    ok(f"{len(sorted_projects)} project{suffix} found.")


def get_name_from_folder() -> str:
    """
    Get the name of the project from the current folder.
    """
    return os.path.basename(os.getcwd())


@requires_pyscript_project_config
def register_project(pyscript_project_config, no_upload=False, confirmed=False):
    """
    Register a project with the API.
    """

    console.print("Contacting the mother ship...")
    project = service.register_project(
        type=pyscript_project_config.get("type", "app"),
        name=pyscript_project_config.get("name", get_name_from_folder()),
        description=pyscript_project_config.get("description", ""),
    )

    write_dot_com_manifest(
        project_id=project["id"],
        user_id=project["user_id"],
        url=project["latest"]["url"],
    )

    if not no_upload:
        console.print("Uploading project files...")
        _upload_project_as_archive(project["id"], confirmed)

    console.print("Uploaded.")


@requires_dot_com_project_id
def create_version(project_id):
    """
    Create a new version of the project.
    """
    data = service.create_version(project_id)
    ok(f"Version {data['version']} created.\nURL: {data['url']}")


@requires_dot_com_project_id
def get_version(project_id, version):
    """
    Get information from the API about the referenced version.
    """
    for key, value in service.get_version(project_id, version).items():
        # Attempt to line things up :)
        tabs = "\t\t" if len(key) < 7 else "\t"
        console.print(f"{key}:{tabs}{value}")
    console.print()
    ok()


@requires_dot_com_project_id
def delete_version(project_id, version):
    """
    Delete the referenced version.
    """
    service.delete_version(project_id, version)
    ok(f"Deleted: {version}")


@requires_dot_com_project_id
def publish_version(project_id, version):
    """
    Publish a version.
    """
    service.publish_version(project_id, version)
    ok("Published")


@requires_dot_com_project_id
def unpublish_version(project_id, version):
    """
    Unpublish a version.
    """
    service.unpublish_version(project_id, version)
    ok("Unpublished")


def display_files_in_table(path_and_metadata, title):
    """
    Helper function for constructing the entries of what to display in
    the files table.
    """
    for_display = []
    for path, file_metadata in path_and_metadata:
        try:
            # this is a remote file
            timestamp = datetime.datetime.strptime(
                file_metadata["updated_at"], "%Y-%m-%dT%H:%M:%S%z"
            )
        except KeyError:
            # this is a local file
            timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(path))

        human_readable_timestamp = convert_timestamp_to_human_readable_time(timestamp)

        for_display.append(
            dict(
                path=path,
                size=str(file_metadata["size"]),
                updated_at=human_readable_timestamp,
            )
        )

    renderers.display_files(for_display, title)


def convert_timestamp_to_human_readable_time(timestamp):
    return timestamp.strftime("%A, %B %d, %Y %I:%M %p")


@requires_dot_com_project_id
def show_project_files_info(project_id):
    """
    Show project files information in 4 different tables.
        - All Remote files present in PyScript.com
        - New files present locally in the project folder
        - Files missing locally from the project folder but present on PyScript.com
        - Files that differ between local project folder and PyScript.com
    """

    diffs = _diff_project_files(project_id)

    remote_files = diffs["remote_files"]
    local_files = diffs["local_files"]
    new_local_files = diffs["new_local_files"]
    local_files_missing = diffs["local_files_missing"]
    files_modified = diffs["files_modified"]

    # Show Remote Files
    remote_paths_and_metadata = []
    for path, file_metadata in remote_files.items():
        remote_paths_and_metadata.append((path, file_metadata))
    display_files_in_table(remote_paths_and_metadata, "Remote Files")

    # Show New Local Files
    local_files_not_present_in_remote = []
    for path in new_local_files:
        file_metadata = local_files[path]
        local_files_not_present_in_remote.append((path, file_metadata))
    display_files_in_table(local_files_not_present_in_remote, "New Local Files")

    # Show Local Files Missing
    remote_files_not_present_in_local = []
    for path in local_files_missing:
        file_metadata = remote_files[path]
        remote_files_not_present_in_local.append((path, file_metadata))
    display_files_in_table(remote_files_not_present_in_local, "Local Files Missing")

    # Show Modified Files
    files_that_differ_in_content = []
    for path in files_modified:
        file_metadata = local_files[path]
        files_that_differ_in_content.append((path, file_metadata))
    display_files_in_table(files_that_differ_in_content, "Files Modified")


@requires_dot_com_project_id
def show_project_versions(project_id):
    """
    Show project versions information
    """
    data = service.list_versions(project_id)
    for each_version in data:
        timestamp = datetime.datetime.strptime(
            each_version["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        each_version["updated_at"] = convert_timestamp_to_human_readable_time(timestamp)
    renderers.display_versions(data)


@requires_dot_com_manifest
def show_project_metadata(manifest):
    """
    Show project metadata information
    """
    renderers.display_manifest(manifest)


def get_file_entries(folder):
    """
    Return a structured dict with the folder [nested] structure.
    """
    ignore = settings.ignore.union(set([settings.hidden_directory]))
    folder_files = {}
    for entry in folder.iterdir():
        if entry.is_file():
            entry_path = f"{folder}/{entry.name}"
            if entry_path in ignore or entry.name in ignore:
                continue

            with open(entry, "rb") as f:
                file_data = f.read()
                possible_hashes = calculate_s3_etag(f)

            folder_files[entry_path] = {
                "entry": entry,
                "size": len(file_data),
                "possible_hashes": possible_hashes,
            }
        else:
            new_entries = get_file_entries(entry)
            folder_files.update(new_entries)

    return folder_files


@requires_dot_com_project_id
def upload_project(project_id, as_archive=False, confirmed=False):
    """
    Upload the project to PyScript.com

    The default is to upload as files, which leads to
    confirmation prompts for 3 different scenarios:
        - Should new files present locally be uploaded?
        - Should files that differ in content be uploaded?
        - Should files be deleted from PyScript.com that are not present locally?

    The other option is to upload the project as an archive, which is
    not user-facing by default and is primarily meant for internal usage.
    Still, one confirmation prompt is offered about:
        - deletion of files from PyScript.com that are not present locally
    """

    if as_archive:
        _upload_project_as_archive(project_id, confirmed)
    else:
        _upload_project_as_files(project_id, confirmed)


def delete_all_projects():
    """
    Delete all projects.
    """
    for project in service.list_projects():
        delete_project_by_id(project["id"])


@requires_dot_com_project_id
def delete_project(project_id):
    """
    Delete the current project.
    """
    delete_project_by_id(project_id)


def delete_project_by_id(project_id):
    """
    Given a project id, delete it.
    """
    success = service.delete_project(project_id)
    if success:
        delete_dot_com_hidden_directory()
        console.print("Project deleted.")


def delete_project_by_slug(project_slug):
    """
    Given a project slug, delete it.
    """
    user_details = service.get_current_user_details()
    user = user_details.get("username", "") or user_details["id"]

    project = service.get_project_by_user_and_slug(user, project_slug)
    project_id = project["id"]

    delete_project_by_id(project_id)


def _download_remote_files(project_path: Path, remote_files: list[str]):
    """
    Given a list of `remote_files`, downloads them in the `project_path`
    on the local machine.
    """

    # Download the files.
    for file_metadata in track(remote_files, "downloading"):
        # The file path is in the form:
        # <user_id>/<project_id>/<version>/<path_of_file>
        # eg: 1282df6f-798e-4b1c-ae1c-5fb8699af762/9e65f5c0-04e0-439d-9cac-2b39eb04e901/v1/hi.py
        # then, `file_path_relative_to_version` is `hi.py`
        file_path_relative_to_version = "/".join(file_metadata["path"].split("/")[3:])

        # The URL to download (on pyscript.com/api).
        url = f"{settings.api_host}{settings.api_base}/content/{file_metadata['path']}"

        # We don't want to recreate the <user_id>/<project_id>/<version> part of the folder
        # structure, so we strip those items off when creating the local file.
        local_file = project_path / file_path_relative_to_version

        # Download it!
        service.download_file(url, local_file)


def download_project_files(project, confirmed):
    """
    Downloads the files associated with a project by creating a new directory for it
    under the current directory.
    """

    project_id = project["id"]
    remote_files = service.list_files(project_id)

    # Create a local folder where we download the project files.
    project_path = Path(project["slug"])

    if project_path.exists():
        console.print(f"Uh oh. Folder {project_path} already exists!", style="red")
        if confirmed:
            console.print(
                "Auto confirmed for deleting the local folder and proceeding with the "
                "download operation."
            )
        else:
            confirmed = typer.confirm(
                f"Do you want to delete the data in the {project_path.absolute()} folder "
                "and proceed with the download operation? (All the data in your current "
                "folder will be lost)"
            )

            if not confirmed:
                raise Abort(
                    f"Oof, that was close! Operation aborted.\nTo avoid complications, "
                    f"delete folder {project_path} or cd into a different folder before "
                    f"downloading project {project['name']} again."
                )

        # If confirmed, we delete the current path.
        shutil.rmtree(project_path)

    console.print(
        f"Downloading project {project['slug']}. "
        f"A total of {len(remote_files)} files will be downloaded.",
        style="green",
    )
    project_path.mkdir(exist_ok=True)

    _download_remote_files(project_path, remote_files)

    # Finally, create the manifest.
    write_dot_com_manifest(
        project_path=project_path,
        project_id=project["id"],
        user_id=project["user_id"],
        url=project["latest"]["url"],
    )

    ok(
        f"Project downloaded successfully, cd into {project['slug']} to use the project."
    )


def download_project_by_user_and_slug(username, project_slug, confirmed):
    """
    Given a username and the project slug, download the project as a new folder
    in the current directory.
    """

    console.print("Fetching project information")

    project = service.get_project_by_user_and_slug(username, project_slug)
    download_project_files(project, confirmed)


def download_project_by_id(project_id, confirmed):
    """
    Given a project id, download it as a new folder in the current directory.
    """

    console.print("Fetching project information")

    project = service.get_project(project_id)
    download_project_files(project, confirmed)


@requires_dot_com_project_id
def download_project_updates(project_id: Optional[str], confirmed: bool) -> None:
    """
    When inside a current project, download updates for it.

    Updates correspond to any local files which are missing i.e.
    they are present remotely but not locally along with any files
    which were modified and differ from what is present on remote.
    """
    diffs = _diff_project_files(project_id)

    files_to_sync = diffs["local_files_missing"].union(diffs["files_modified"])

    if not files_to_sync:
        ok("Nothing to download \U0001F44D")
        return

    _print_new_local_files(diffs)
    _print_files_modified(diffs)
    _print_local_files_missing(diffs)

    if confirmed:
        console.print(
            "Auto confirmed for update local project with changes present in pyscript.com"
        )
    else:
        confirmed = typer.confirm(
            "Do you want to update the local project with changes present in pyscript.com?\n"
            "(this will not delete any local file which is not present in pyscript.com)"
        )
        if not confirmed:
            raise Abort("Ok. Operation aborted.")

    console.print("Downloading files...")
    console.print()

    files_metadata = []
    for each_file in files_to_sync:
        files_metadata.append(diffs["remote_files"][each_file])

    _download_remote_files(project_path=Path("."), remote_files=files_metadata)


@requires_dot_com_manifest
def view_project(manifest, version=None):
    """
    View the current project at its URL.
    """
    if "url" not in manifest:
        raise Abort(
            "Cannot view this project as it is not hosted at pyscript.com\n"
            "Please remember to upload your project (pyscript upload)."
        )

    url = manifest["url"]

    if version:
        project_id = manifest["project_id"]
        # this call will abort execution if version is invalid
        service.get_version(project_id, version)

        url = url.replace("/latest", f"/{version}")
    else:
        # If no version is provided we need to strip the version section of the url
        # NOTE: We are assuming that url will always end with `/`

        parts = url.split("/")
        # Parts: ['https:', '', 'account.pyscriptapps-dev.com', 'application-test', 'version', '']
        # Now grab the http(s) portion and join it with the domain+slug
        url = f"{parts[0]}//{'/'.join(parts[2:-2])}/"

    console.print("Opening url:", url)
    webbrowser.open_new_tab(url)

    ok()


def copy_project_utils(
    project: dict, new_name: str, download: bool = False, confirmed: bool = False
):
    """
    Given a project and a new name, makes a copy of it
    in the PyScript.com account. Also downloads it locally
    to the current directory if `download` is True.
    """
    # extract name and id from project to be copied...
    project_name = project["name"]
    project_id = project["id"]

    # set the new name
    project["name"] = new_name or f"{project_name} copy"

    # copy the project
    copied_project = service.copy_project(project_id, project["name"])

    console.print(
        f"[bold]Project successfully copied with id: {copied_project['id']}[/bold]"
    )
    if download:
        # download the copy locally if --download is set
        download_project_files(copied_project, confirmed)
    else:
        ok()


@requires_dot_com_project_id
def copy_from_inside_project(project_id, new_name):
    copy_project_by_id(project_id, new_name, download=False)


def copy_project_by_id(project_id, new_name, download=False, confirmed=False):
    """
    Copy a project by project id. The copy has the name `new_name` (if supplied)
    or defaults to using the old name with `copy` suffixed to it.
    Eg: `mpl` --> `mpl copy`
    The option --download (if set) allows to also download files locally along with
    making a copy in the PyScript.com account.
    """

    project = service.get_project(project_id)
    copy_project_utils(project, new_name, download, confirmed)


def copy_project_by_username_and_slug(
    username, project_slug, new_name, download=False, confirmed=False
):
    """
    Copy a project by username and project slug.
    The copy has the name `new_name` (if supplied)
    or defaults to using the old name with `copy` suffixed to it.
    Eg: `mpl` --> `mpl copy`
    The option --download (if set) allows to also download files locally along with
    making a copy in the PyScript.com account.
    """

    project = service.get_project_by_user_and_slug(username, project_slug)
    copy_project_utils(project, new_name, download, confirmed)


# Internal #############################################################################


def _diff_project_files(project_id: str) -> dict:
    """
    Calculate files that have been added / removed / modified

    Args:
        project_id (str): Project ID for which to calculate differences

    Returns:
        (dict): A dictionary containing the following keys:
            - local_files: metadata dict for local files
            - remote_files: metadata dict for remote files
            - new_local_files: metadata dict for files present locally but not in remote
            - local_files_missing: metadata dict for files present remotely but not locally
            - files_in_both: metadata dict for files which are present
                             both remotely as well as locally
            - files_modified: metadata dict for files which are present in both
                              but their hashes don't match
    """

    remote_files = _get_remote_files(project_id)
    local_files = _get_local_files()

    new_local_files = set(local_files).difference(remote_files)
    local_files_missing = set(remote_files).difference(local_files)
    files_in_both = set(local_files).intersection(remote_files)

    def is_file_modified(filepath):
        assert filepath in files_in_both
        local_file = local_files[filepath]
        remote_file = remote_files[filepath]
        return remote_file["hash"] not in local_file["possible_hashes"]

    files_modified = set()
    for each_file in files_in_both:
        if is_file_modified(each_file):
            files_modified.add(each_file)

    return {
        "local_files": local_files,
        "remote_files": remote_files,
        "new_local_files": new_local_files,
        "local_files_missing": local_files_missing,
        "files_in_both": files_in_both,
        "files_modified": files_modified,
    }


def _print_new_local_files(diffs):
    """
    Print information about new files present locally.

    Args:
        diffs (dict): The object containing information about differences between files
                      present remotely and locally. This is the output of the `_diff_project_files`
                      function.

    Returns:
        None
    """
    console.print(
        f"Found {len(diffs['new_local_files'])} new files present locally, "
        "but not on pyscript.com:",
        style="bold green",
    )
    for entry in diffs["new_local_files"]:
        console.print(f"\t- {entry}")
    console.print()


def _print_files_modified(diffs):
    """
    Print information about files that have been modified.

    Args:
        diffs (dict): The object containing information about differences between files
                      present remotely and locally. This is the output of the `_diff_project_files`
                      function.

    Returns:
        None
    """
    console.print(
        f"Found {len(diffs['files_modified'])} files locally that differ in content from "
        "what is present on pyscript.com:",
        style="bold green",
    )
    for entry in diffs["files_modified"]:
        console.print(f"\t- {entry}")
    console.print()


def _print_local_files_missing(diffs):
    """
    Print information about files that are present in PyScript.com but are missing locally.

    Args:
        diffs (dict): The object containing information about differences between files
                      present remotely and locally. This is the output of the `_diff_project_files`
                      function.

    Returns:
        None
    """
    console.print(
        f"Found {len(diffs['local_files_missing'])} files present on "
        "pyscript.com, but not locally:",
        style="bold red",
    )
    for entry in diffs["local_files_missing"]:
        console.print(f"\t- {entry}", style="bold red")
    console.print()


def _get_remote_files(project_id):
    """Get metadata for the remote project files.

    Returns a list of dictionaries in the form:

    {
        <path> : <file metadata>
    }

    """

    entries = service.list_files(project_id)

    return {"/".join(Path(entry["path"]).parts[3:]): entry for entry in entries}


def _get_local_files():
    """Get metadata for the local project files.

    Returns a list of dictionaries in the form:

    {
        "entry": <file name>,
        "size": number of bytes,
        "possible_hashes": the possible hashes (S3 etag) for the file.
    }

    """

    ignore = settings.ignore.union(set([settings.hidden_directory]))

    local_files = {}
    for entry in Path().iterdir():
        if entry.name in ignore:
            continue

        if entry.is_file():
            with open(entry, "rb") as f:
                file_data = f.read()
                possible_hashes = calculate_s3_etag(f)

            local_files[entry.name] = {
                "entry": entry,
                "size": len(file_data),
                "possible_hashes": possible_hashes,
            }

        else:
            entries = get_file_entries(entry)
            local_files.update(entries)

    return local_files


def _upload_project_as_archive(project_id, confirmed):
    """
    Upload the project contents to pyscript.com as a zip archive.
    Also allow deletion of files present in remote but not locally
    via a separate prompt.
    """

    diffs = _diff_project_files(project_id)

    files_to_sync = (
        diffs["new_local_files"]
        .union(diffs["files_modified"])
        .union(diffs["local_files_missing"])
    )

    if not files_to_sync:
        ok("Nothing to upload \U0001F44D")
        return

    _print_new_local_files(diffs)
    _print_files_modified(diffs)

    if len(diffs["new_local_files"]) or len(diffs["files_modified"]):
        console.print("Uploading new as well as modified files present locally.")

    # Create a temporary directory.
    temp_root = Path(tempfile.TemporaryDirectory().name)
    temp_dir = temp_root / "pyscript_project"
    # Copy the contents of the project into temp directory,
    # while ignoring .files (like .git, .pytest_cache) and *.pyc etc...
    shutil.copytree(
        Path(),
        temp_dir,
        ignore=shutil.ignore_patterns(
            settings.hidden_directory, *settings.archive_ignore
        ),
    )
    # Zip up the temporary directory.
    archive = Path(f"{settings.archive_name}.{settings.archive_format}")
    shutil.make_archive(settings.archive_name, settings.archive_format, temp_dir)
    # Upload to the API as an archive.
    with archive.open("rb") as f:
        service.upload_archive(project_id, f)
    # Clean up / delete the temporary directory.
    shutil.rmtree(temp_dir)
    archive.unlink()

    confirmed_for_deleting_files = confirmed

    if len(diffs["local_files_missing"]):
        _print_local_files_missing(diffs)
        if confirmed:
            console.print(
                "Auto confirmed for deleting files from pyscript.com that are not present "
                "locally..."
            )
        else:
            confirmed_for_deleting_files = typer.confirm(
                "Do you want to delete files from pyscript.com that are not present locally?"
            )
        console.print()

    if confirmed_for_deleting_files:
        for filepath in diffs["local_files_missing"]:
            service.delete_file(project_id, filepath)
            console.print(f"{filepath} deleted from pyscript.com \u2705")

    ok("\nTo see your changes online type: pyscript view")


def _upload_project_as_files(project_id, confirmed):
    """
    Diff and upload files individually.
    Also allow deletion of files present in remote but not locally
    via a separate prompt.
    """

    diffs = _diff_project_files(project_id)

    files_to_sync = (
        diffs["new_local_files"]
        .union(diffs["files_modified"])
        .union(diffs["local_files_missing"])
    )

    if not files_to_sync:
        ok("Nothing to upload \U0001F44D")
        return

    confirmed_for_new_files = confirmed
    confirmed_for_modified_files = confirmed
    confirmed_for_deleting_files = confirmed

    if len(diffs["new_local_files"]):
        _print_new_local_files(diffs)
        if confirmed:
            console.print("Auto confirmed for uploading new files present locally...")
        else:
            confirmed_for_new_files = typer.confirm(
                "Do you want to upload new files present locally?"
            )
        console.print()
    if len(diffs["files_modified"]):
        _print_files_modified(diffs)
        if confirmed:
            console.print(
                "Auto confirmed for uploading modified files present locally..."
            )
        else:
            confirmed_for_modified_files = typer.confirm(
                "Do you want to upload files that have changed?"
            )
        console.print()
    if len(diffs["local_files_missing"]):
        _print_local_files_missing(diffs)
        if confirmed:
            console.print(
                "Auto confirmed for deleting files from pyscript.com that are not present "
                "locally..."
            )
        else:
            confirmed_for_deleting_files = typer.confirm(
                "Do you want to delete files from pyscript.com that are not present locally?"
            )
        console.print()

    show_message = any(
        [
            confirmed_for_new_files,
            confirmed_for_modified_files,
            confirmed_for_deleting_files,
        ]
    )

    if show_message:
        console.print("Uploading files...")
        console.print()

    if confirmed_for_new_files:
        for filepath in diffs["new_local_files"]:
            with open(filepath, "rb") as f:
                service.upload_file(project_id, f)
                console.print(f"{filepath} uploaded to pyscript.com \u2705")

    if confirmed_for_modified_files:
        for filepath in diffs["files_modified"]:
            with open(filepath, "rb") as f:
                service.upload_file(project_id, f, override=True)
                console.print(f"{filepath} uploaded to pyscript.com \u2705")

    if confirmed_for_deleting_files:
        for filepath in diffs["local_files_missing"]:
            service.delete_file(project_id, filepath)
            console.print(f"{filepath} deleted from pyscript.com \u2705")

    if show_message:
        ok(
            "Files uploaded successfully \U0001F44D"
            "\nTo see your changes online type: pyscript view"
        )


def create_project_configuration():
    """
    Create a new project configuration file.
    """
    console.print("Creating a new project configuration file.")
    console.print(
        "Please answer the following questions to create a new project configuration file."
    )

    # Defaulting to "app" for now since the pyscript cli only supports this
    # type for now.
    project_type = "app"
    # project_type = Prompt.ask(
    #     "What type of project is this? (app)",
    #     choices=["app", "library", "other"],
    #     default="app",
    # )
    project_name = Prompt.ask(
        "What is the name of the project?", default="my-pyscript-app"
    )
    project_description = Prompt.ask(
        "Please provide a brief description of the project.", default=""
    )

    configuration_type = Prompt.ask(
        "What extension would you like to use for the configuration file?",
        choices=["json", "toml"],
        default="toml",
    )

    project_config = {
        "type": project_type,
        "name": project_name,
        "description": project_description,
    }

    if configuration_type == "json":
        configuration_name = "pyscript.json"
    else:
        configuration_name = "pyscript.toml"

    # Write the project configuration file.
    with open(configuration_name, "w") as f:
        if configuration_type == "json":
            json.dump(project_config, f, indent=2)
        else:
            contents = f'name = "{project_name}"\ntype = "{project_type}"\n'
            if project_description:
                contents += f'description = "{project_description}"\n'

        f.write(contents)

    project_config_file_path = Path("pyscript.json").resolve()
    console.print(
        f"Project configuration file created at {project_config_file_path}",
        style="green",
    )

    return project_config

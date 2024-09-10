"""
Exercises the API based calls in the api module.

Some of these tests are decorated with @pytest.mark.vcr. For more information,
please see: https://github.com/kiwicom/pytest-recording

If you add new tests that require API interactions recording:

$ pytest --record-mode=once

The API will be hit over the network, but traffic will be stored in a YAML file
in the cassettes subdirectory.

To regenerate the cassette recordings for all the API tests:

$ pytest --record-mode=all

Otherwise, using pytest without the --record-mode set will skip hitting the
actual API and re-play the API interactions stored in the YAML files in the
cassettes directory.
"""

import json
import os
import time
from pathlib import Path
from unittest import mock

import pytest
from typer.testing import CliRunner

from pyscript import app
from pyscript import config as core_config
from pyscript_dot_com import cli, service
from pyscript_dot_com.config import settings

from .conftest import FAKE_USERNAME

cli.auth.KEYRING_APP_NAME = "pyscript_dot_com_tests"


def invoke_cli(args, **kwargs):
    """Invoke a CLI command."""

    runner = CliRunner()
    return runner.invoke(app, args, **kwargs)


# Fixtures #############################################################################


@pytest.fixture
def registered_local_app(hostname, local_app, ok):
    """
    Convenience fixture to:

    1) delete all the user's projects.
    2) change into the local test app directory.
    3) register the local test app.

    """

    cli.delete_all_projects()
    os.chdir(local_app)

    yield cli.register_project()


@pytest.fixture
def logged_in_user(hostname, fake_but_valid_user_jwt_token):
    """Fake that the user has logged in."""

    from pyscript_dot_com.auth import _store_credentials

    _store_credentials(fake_but_valid_user_jwt_token)


@pytest.fixture
def ok():
    """Mock the rich ok call."""

    with mock.patch("pyscript_dot_com.cli.ok") as mock_ok:
        yield mock_ok


@pytest.fixture
def prevent_login(monkeypatch, mock_webbrowser, mock_handle_request, auto_enter):
    """Make calls to cli.login fail."""

    def get_credentials_from_platform(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "pyscript_dot_com.auth.get_credentials_from_platform",
        get_credentials_from_platform,
    )


@pytest.fixture
def webbrowser():
    with mock.patch("pyscript_dot_com.cli.webbrowser") as mock_webbrowser:
        yield mock_webbrowser


# Tests ################################################################################


@pytest.mark.vcr
def test_setup_happy_path(
    hostname,
    mock_webbrowser,
    mock_handle_request,
    fake_auth_server,
    auto_enter,
    ok,
    auto_confirm,
):
    """
    A successful setup results in an "ok" message.
    """

    invoke_cli("setup")
    assert ok.call_args("You are all set, go and make history!")


@pytest.mark.vcr
def test_login(
    hostname, mock_webbrowser, mock_handle_request, fake_auth_server, auto_enter, ok
):
    """
    A successful login results in an "ok" message.
    """

    invoke_cli("login")

    called_with_url = mock_webbrowser.open.call_args[0][0]

    assert settings.api_host in called_with_url
    assert "/api/auth/login" in called_with_url


@pytest.mark.vcr
def test_login_fail(hostname, prevent_login):
    """
    An unsuccessful login results in an abort.
    """

    result = invoke_cli("login")

    assert "Could not complete logging you in" in result.output


def test_logout(hostname, ok):
    """
    Logout results in an "ok" message.
    """

    invoke_cli("logout")

    ok.assert_called_once_with("See you soon!")


@pytest.mark.vcr
def test_ping(logged_in_user, ok):
    """
    Correctly configured, ping returns an "ok" pong message.
    """

    invoke_cli("ping")
    ok.assert_called_once_with("Pong.")


@pytest.mark.vcr
def test_list_no_projects(logged_in_user, ok):
    """
    Listing the user's apps results in an "ok" message.
    """

    cli.delete_all_projects()
    ok.reset_mock()

    invoke_cli("list")

    # Since we deleted them all while setting up the context, the test user has
    # no existing projects on the API server.
    ok.assert_called_once_with("0 projects found.")


@pytest.mark.vcr
def test_list_projects(logged_in_user, ok, registered_local_app, app_name):
    """
    Listing the user's apps results in an "ok" message.
    """

    ok.reset_mock()

    result = invoke_cli("list")

    assert app_name in result.output
    ok.assert_called_once_with("1 project found.")


@pytest.mark.skip(reason="algolia search is now live in dev so we get spurious hits")
@pytest.mark.vcr
def test_search_projects(hostname, logged_in_user, ok, registered_local_app, app_name):
    """
    Listing the user's apps results in an "ok" message.
    """

    ok.reset_mock()

    invoke_cli('list --search="no project should match this"')
    ok.assert_called_once_with("0 projects found.")

    # TODO: The backend uses Algolia Search which indexes documents asynchronously.
    # Hence, we don't know how long it will take until the project will actually appear
    # in the search.
    time.sleep(10)

    invoke_cli(f'list --search="{app_name}"')

    ok.assert_called_with("1 project found.")


@pytest.mark.vcr
def test_delete_inside_project_folder(
    logged_in_user, ok, registered_local_app, auto_confirm
):
    ok.reset_mock()

    resp = invoke_cli("list")
    assert "test-application" in resp.stdout

    resp = invoke_cli("delete")

    assert resp.exit_code == 0

    assert (
        "Project deleted from pyscript.com and the local folder has been unlinked"
        in resp.stdout
    )
    assert "To delete local files, run `rm -r test_application` " in resp.stdout

    assert ok.call_count == 1

    # Make sure we clean up the pyscript.com hidden directory.
    assert not Path(settings.hidden_directory).is_dir()

    # using the method below instead of `invoke_cli("list")` since
    # the latter gives a stale and incorrect output
    assert service.list_projects() == []


@pytest.mark.vcr
def test_delete_inside_project_folder_with_auto_confirm(
    logged_in_user, ok, registered_local_app
):
    ok.reset_mock()

    resp = invoke_cli("list")
    assert "test-application" in resp.stdout

    resp = invoke_cli("delete --yes")

    assert resp.exit_code == 0

    assert (
        "Project deleted from pyscript.com and the local folder has been unlinked"
        in resp.stdout
    )
    assert "To delete local files, run `rm -r test_application` " in resp.stdout

    assert ok.call_count == 1

    # Make sure we clean up the pyscript.com hidden directory.
    assert not Path(settings.hidden_directory).is_dir()

    # using the method below instead of `invoke_cli("list")` since
    # the latter gives a stale and incorrect output
    assert service.list_projects() == []


@pytest.mark.vcr
def test_delete_project_by_slug(
    monkeypatch, logged_in_user, ok, registered_local_app, auto_confirm
):
    ok.reset_mock()

    resp = invoke_cli("list")
    assert "test-application" in resp.stdout

    invoke_cli("delete test-application")

    assert ok.call_count == 1

    # Make sure we clean up the pyscript.com hidden directory.
    assert not Path(settings.hidden_directory).is_dir()

    # using the method below instead of `invoke_cli("list")` since
    # the latter gives a stale and incorrect output
    assert service.list_projects() == []


@pytest.mark.vcr
def test_delete_project_by_slug_with_auto_confirm(
    monkeypatch, logged_in_user, ok, registered_local_app
):
    ok.reset_mock()

    resp = invoke_cli("list")
    assert "test-application" in resp.stdout

    invoke_cli("delete test-application --yes")

    assert ok.call_count == 1

    # Make sure we clean up the pyscript.com hidden directory.
    assert not Path(settings.hidden_directory).is_dir()

    # using the method below instead of `invoke_cli("list")` since
    # the latter gives a stale and incorrect output
    assert service.list_projects() == []


@pytest.mark.vcr
def test_delete_project_by_id(
    monkeypatch, logged_in_user, ok, registered_local_app, auto_confirm
):
    """
    Deleting the app from the server results in an "ok" message.
    """

    ok.reset_mock()

    resp = invoke_cli("list")
    assert "test-application" in resp.stdout

    with open(settings.manifest_path, "r") as manifest:
        data = json.load(manifest)

    invoke_cli(f"delete {data.get('project_id')}")

    assert ok.call_count == 1

    # Make sure we clean up the pyscript.com hidden directory.
    assert not Path(settings.hidden_directory).is_dir()

    # using the method below instead of `invoke_cli("list")` since
    # the latter gives a stale and incorrect output
    assert service.list_projects() == []


@pytest.mark.vcr
def test_delete_project_by_id_with_auto_confirm(
    monkeypatch, logged_in_user, ok, registered_local_app
):
    """
    Deleting the app from the server results in an "ok" message.
    """

    ok.reset_mock()

    resp = invoke_cli("list")
    assert "test-application" in resp.stdout

    with open(settings.manifest_path, "r") as manifest:
        data = json.load(manifest)

    invoke_cli(f"delete {data.get('project_id')} --yes")

    assert ok.call_count == 1

    # Make sure we clean up the pyscript.com hidden directory.
    assert not Path(settings.hidden_directory).is_dir()

    # using the method below instead of `invoke_cli("list")` since
    # the latter gives a stale and incorrect output
    assert service.list_projects() == []


@pytest.mark.vcr
def test_create_version(logged_in_user, ok, registered_local_app, app_name):
    """
    Ensure the expected version is created.
    """

    ok.reset_mock()

    invoke_cli("version create")

    assert ok.call_count == 1
    assert "Version v1 created" in ok.call_args[0][0]

    resp = invoke_cli("version list")
    assert "v1" in resp.stdout


@pytest.mark.vcr
def test_get_version(logged_in_user, ok, registered_local_app):
    """
    Get the expected data about the released version.
    """

    version = "v1"
    cli.create_version()
    ok.reset_mock()

    with open(settings.manifest_path, "r") as manifest:
        data = json.load(manifest)

    result = invoke_cli(f"version info {version}")

    expected_values = {"user_id": data["user_id"], "project_id": data["project_id"]}

    # Assert: sanity check the console output (not exhaustive, but good enough).
    for each_line in result.output.split("\n"):
        for key in expected_values.keys():
            if each_line.startswith(key):
                value = each_line.split(":")[1].strip()
                # checking for `in` instead of `==` because of richly formatted text
                assert expected_values[key] in value


@pytest.mark.vcr
def test_delete_version(logged_in_user, ok, registered_local_app):
    """
    Delete the referenced version.
    """

    version = "v1"
    cli.create_version()
    ok.reset_mock()

    with open(settings.manifest_path, "r") as manifest:
        data = json.load(manifest)

    invoke_cli(f"version delete {version}")

    ok.assert_called_once_with(f"Deleted: {version}")

    data = service.list_versions(data["project_id"])
    all_versions = [d["version"] for d in data]
    assert version not in all_versions


@pytest.mark.vcr
def test_view_project(hostname, logged_in_user, ok, registered_local_app, webbrowser):
    """
    Ensure the expected URL is opened in the browser.
    """

    ok.reset_mock()

    invoke_cli("view")

    expected_url = (
        "https://test_account_do_not_delete.pyscriptapps-dev.com/test-application/"
    )

    webbrowser.open_new_tab.assert_called_once_with(expected_url)
    assert ok.call_count == 1


@pytest.mark.vcr
def test_view_project_doesnt_remove_slug_sections(
    hostname, logged_in_user, ok, registered_local_app, webbrowser
):
    """
    Ensure the expected URL is opened in the browser.
    """

    ok.reset_mock()

    invoke_cli("view")

    # We expect that the URL doesn't contain the '/latest' part which is the version
    expected_url = (
        "https://test_account_do_not_delete.pyscriptapps-dev.com/test-application/"
    )

    webbrowser.open_new_tab.assert_called_once_with(expected_url)
    assert ok.call_count == 1


@pytest.mark.vcr
def test_view_project_doesnt_remove_slug_sections_if_version_other_than_latest(
    hostname, logged_in_user, ok, registered_local_app, webbrowser
):
    """
    Ensure the expected URL is opened in the browser.
    """

    ok.reset_mock()

    invoke_cli("view")

    # We expect that the URL doesn't contain the '/version' part which is the version
    # for this test
    expected_url = (
        "https://test_account_do_not_delete.pyscriptapps-dev.com/test-application/"
    )

    webbrowser.open_new_tab.assert_called_once_with(expected_url)
    assert ok.call_count == 1


@pytest.mark.vcr
def test_view_project_invalid_version(
    hostname, logged_in_user, ok, registered_local_app, webbrowser
):
    """
    Expect an error and URL is not opened in the browser
    """

    ok.reset_mock()

    version = "invalid-version"

    resp = invoke_cli(f"view {version}")
    assert resp.exit_code == 1
    assert "Aborted" in resp.stdout

    assert webbrowser.open_new_tab.call_count == 0
    assert ok.call_count == 0


@pytest.mark.vcr
def test_view_specific_version_of_project(
    hostname, logged_in_user, ok, registered_local_app, webbrowser
):
    """
    Ensure the expected URL is opened in the browser.
    """

    version = "v1"
    cli.create_version()
    ok.reset_mock()

    invoke_cli(f"view {version}")

    with open(settings.manifest_path, "r") as manifest:
        data = json.load(manifest)

    url = data.get("url").replace("/latest", f"/{version}")
    webbrowser.open_new_tab.assert_called_once_with(url)

    assert ok.call_count == 1


@pytest.mark.vcr
def test_copy(hostname, logged_in_user, ok, registered_local_app, app_name):
    """
    Ensure that copying a project generate the expected results
    """

    # we can read the id from the newly created manifest
    with open(settings.manifest_path) as manifest:
        data = json.load(manifest)
    app_id = data.get("project_id")

    ok.reset_mock()
    new_app_name = f"copied_{app_name}"

    invoke_cli(f"copy {app_id} {new_app_name}")

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 2

    original, copy = data[app_name], data[new_app_name]
    for key in ["user_id", "description", "type"]:
        assert original[key] == copy[key]
    for key in ["created_at", "updated_at"]:
        assert original[key] < copy[key]
    for key in ["id", "name"]:
        assert original[key] != copy[key]
    assert ok.call_count == 1  # once for copy confirmation.


@pytest.mark.vcr
def test_copy_auto_confirm(
    hostname, logged_in_user, ok, registered_local_app, app_name
):
    """
    Ensure that copying a project generate the expected results
    """

    # we can read the id from the newly created manifest
    with open(settings.manifest_path) as manifest:
        data = json.load(manifest)
    app_id = data.get("project_id")

    ok.reset_mock()
    new_app_name = f"copied_{app_name}"

    invoke_cli(f"copy {app_id} {new_app_name} --yes")

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 2

    original, copy = data[app_name], data[new_app_name]
    for key in ["user_id", "description", "type"]:
        assert original[key] == copy[key]
    for key in ["created_at", "updated_at"]:
        assert original[key] < copy[key]
    for key in ["id", "name"]:
        assert original[key] != copy[key]
    assert ok.call_count == 1  # once for copy confirmation.


@pytest.mark.vcr(allow_playback_repeats=True)
def test_copy_with_download(
    hostname, logged_in_user, ok, registered_local_app, app_name, tmp_path
):
    """
    Ensure that copying a project generate the expected results and also downloads files
    """

    cli.upload_project(as_archive=True)

    # we can read the id from the newly created manifest
    with open(settings.manifest_path) as manifest:
        data = json.load(manifest)

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    app_id = data.get("project_id")
    new_app_name = f"copied_{app_name}"

    invoke_cli(f"copy {app_id} {new_app_name} --download")

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 2

    original, copy = data[app_name], data[new_app_name]
    for key in ["user_id", "description", "type"]:
        assert original[key] == copy[key]
    for key in ["created_at", "updated_at"]:
        assert original[key] < copy[key]
    for key in ["id", "name"]:
        assert original[key] != copy[key]

    # we expect to have a local copy to the project
    new_app_path = target_dir / copy["slug"]
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        new_file = new_app_path / filename
        assert new_file.exists()

    assert ok.call_count == 1  # once for copy confirmation.


@pytest.mark.vcr
def test_upload_project(hostname, logged_in_user, ok, local_app, auto_confirm):
    """
    Uploading project files to the API behaves as expected.
    """

    cli.delete_all_projects()
    os.chdir(local_app)
    ok.reset_mock()

    resp = invoke_cli("upload")
    assert "Uploading new as well as modified files present locally." in resp.stdout
    assert "Uploaded" in resp.stdout

    resp = service.list_projects()
    assert len(resp) == 1

    assert ok.call_count == 1
    assert "To see your changes online type: pyscript view" in ok.call_args[0][0]


@pytest.mark.vcr
def test_upload_project_no_project_config(
    hostname, logged_in_user, ok, local_app, auto_confirm, auto_enter
):
    """
    Uploading project files to the API behaves as expected.
    """

    cli.delete_all_projects()
    os.chdir(local_app)
    os.remove(core_config["project_config_filename"])
    ok.reset_mock()

    resp = invoke_cli("upload")
    assert "Uploading new as well as modified files present locally." in resp.stdout
    assert "Uploaded" in resp.stdout

    resp = service.list_projects()
    assert len(resp) == 1

    assert ok.call_count == 1
    assert "To see your changes online type: pyscript view" in ok.call_args[0][0]

    # Open the created project config file and check its contents
    with open(core_config["project_config_filename"], "r") as f:
        data = f.read()

    assert 'name = "my-pyscript-app"' in data
    assert 'type = "app"' in data


@pytest.mark.vcr
def test_upload_project_with_auto_confirm(hostname, logged_in_user, ok, local_app):
    """
    Uploading project files to the API behaves as expected.
    """

    cli.delete_all_projects()
    os.chdir(local_app)
    ok.reset_mock()

    resp = invoke_cli("upload --yes")
    assert "Uploading new as well as modified files present locally." in resp.stdout
    assert "Uploaded" in resp.stdout

    resp = service.list_projects()
    assert len(resp) == 1

    assert ok.call_count == 1
    assert "To see your changes online type: pyscript view" in ok.call_args[0][0]


@pytest.mark.vcr
def test_upload_project_overrides_file_successfully(
    hostname, logged_in_user, ok, local_app, auto_confirm
):
    """
    Uploading project files to the API behaves as expected.
    """

    cli.delete_all_projects()
    os.chdir(local_app)
    ok.reset_mock()

    resp = invoke_cli("upload")
    assert "Uploading new as well as modified files present locally." in resp.stdout
    assert "Uploaded" in resp.stdout

    resp = service.list_projects()
    assert len(resp) == 1

    assert ok.call_count == 1
    assert "To see your changes online type: pyscript view" in ok.call_args[0][0]

    # Now change the local_app to change the main.py file
    with open("main.py", "a") as f:
        f.write("\n# added a comment")

    # Now call upload again
    resp = invoke_cli("upload")
    assert (
        "Found 1 files locally that differ in content from what is present"
        in resp.stdout
    )
    assert "main.py uploaded" in resp.stdout

    resp = service.list_projects()
    assert len(resp) == 1

    assert ok.call_count == 2
    assert "To see your changes online type: pyscript view" in ok.call_args[0][0]

    # Now revert the change and call upload again
    with open("main.py", "r") as f:
        lines = f.readlines()
    with open("main.py", "w") as f:
        f.writelines(lines[:-2])

    resp = invoke_cli("upload")

    resp = service.list_projects()
    assert len(resp) == 1


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_by_username_and_slug(
    logged_in_user,
    ok,
    local_app,
    app_name,
    tmp_path,
    auto_confirm,
):
    # project should already exist before downloading it
    existing_projects = service.list_projects()
    assert len(existing_projects) == 1

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    slug = "test-application"
    invoke_cli(f"download @{FAKE_USERNAME}/{slug}")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.
    assert "Project downloaded successfully" in ok.call_args[0][0]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        old_file = local_app / filename
        new_file = new_app_path / filename
        assert new_file.exists()
        assert open(old_file).read() == open(new_file).read()


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_by_id(logged_in_user, ok, app_name, tmp_path, auto_confirm):
    """
    Downloading an app from the server results in an "ok" message and app files have been
    downloaded.
    """

    # project should already exist before downloading it
    existing_projects = service.list_projects()
    assert len(existing_projects) == 1
    project_id = existing_projects[0]["id"]

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    invoke_cli(f"download {project_id}")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.
    assert "Project downloaded successfully" in ok.call_args[0][0]

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 1
    slug = data[app_name]["slug"]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        new_file = new_app_path / filename
        assert new_file.exists()


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_by_id_with_auto_confirm(
    logged_in_user, ok, app_name, tmp_path
):
    """
    Downloading an app from the server results in an "ok" message and app files have been
    downloaded.
    """

    # project should already exist before downloading it
    existing_projects = service.list_projects()
    assert len(existing_projects) == 1
    project_id = existing_projects[0]["id"]

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    invoke_cli(f"download {project_id} --yes")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.
    assert "Project downloaded successfully" in ok.call_args[0][0]

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 1
    slug = data[app_name]["slug"]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        new_file = new_app_path / filename
        assert new_file.exists()


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_by_psadc_url(
    logged_in_user, ok, app_name, tmp_path, auto_confirm
):
    """
    Downloading an app from the server results in an "ok" message and app files have been
    downloaded.
    """

    # project should already exist before downloading it
    existing_projects = service.list_projects()
    assert len(existing_projects) == 1
    project_url = existing_projects[0]["latest"]["url"]

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    invoke_cli(f"download {project_url}")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.
    assert "Project downloaded successfully" in ok.call_args[0][0]

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 1
    slug = data[app_name]["slug"]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        new_file = new_app_path / filename
        assert new_file.exists()


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_by_url(logged_in_user, ok, app_name, tmp_path, auto_confirm):
    """
    Downloading an app from the server results in an "ok" message and app files have been
    downloaded.
    """

    # project should already exist before downloading it
    existing_projects = service.list_projects()
    assert len(existing_projects) == 1
    project_url = "https://test_account_do_not_delete.pyscriptapps-dev.com/test-application/latest"

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    invoke_cli(f"download {project_url}")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.
    assert "Project downloaded successfully" in ok.call_args[0][0]

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 1
    slug = data[app_name]["slug"]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        new_file = new_app_path / filename
        assert new_file.exists()


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_by_slug_only(
    logged_in_user, ok, app_name, tmp_path, auto_confirm
):
    """
    Downloading an app from the server results in an "ok" message and app files have been
    downloaded.
    """

    # project should already exist before downloading it
    existing_projects = service.list_projects()
    assert len(existing_projects) == 1
    project_slug = existing_projects[0]["slug"]

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    invoke_cli(f"download {project_slug}")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.
    assert "Project downloaded successfully" in ok.call_args[0][0]

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 1
    slug = data[app_name]["slug"]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in ["index.html", "main.py", core_config["project_config_filename"]]:
        new_file = new_app_path / filename
        assert new_file.exists()


@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_updates(
    logged_in_user, ok, registered_local_app, app_name, auto_confirm
):
    cli.upload_project(as_archive=True)

    ok.reset_mock()

    resp = invoke_cli("download")

    assert "Synchronizing files" not in resp.stdout
    assert "downloading" not in resp.stdout
    assert ok.call_count == 1


@pytest.mark.xfail(reason="This test is currently failing and we need to sort it.")
@pytest.mark.vcr(allow_playback_repeats=True)
def test_download_project_containing_images(
    logged_in_user, ok, registered_local_app, app_name, tmp_path, auto_confirm
):
    with open("a.img", "wb") as fp:
        fp.write(b"\xff\xd8\xff")

    cli.upload_project(as_archive=True)

    with open(settings.manifest_path) as manifest:
        data = json.load(manifest)

    target_dir = tmp_path / "empty-dir-to-put-the-download-in"
    target_dir.mkdir()
    os.chdir(target_dir)

    ok.reset_mock()

    invoke_cli(f"download {data['project_id']}")

    # ... after downloading the project.
    assert ok.call_count == 1  # once for download confirmation.

    apps = service.list_projects()
    data = {app["name"]: app for app in apps}
    assert len(data) == 1
    slug = data[app_name]["slug"]

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()

    # we expect to have a local copy to the project
    new_app_path = target_dir / slug
    assert new_app_path.exists()
    for filename in [
        "index.html",
        "main.py",
        core_config["project_config_filename"],
        "a.img",
    ]:
        new_file = new_app_path / filename
        assert new_file.exists()

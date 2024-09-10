"""
Exercises the Ory-based authentication (auth) functions.

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

import keyring
import pytest

from pyscript_dot_com import auth

auth.KEYRING_APP_NAME = "pyscript_dot_com_tests"


@pytest.fixture(autouse=True)
def clear_keyring():
    """
    Clear the test keyring.
    """

    for key in ["hostname", "prefix"]:
        try:
            keyring.delete_password(auth.KEYRING_APP_NAME, key)
        except keyring.errors.PasswordDeleteError:
            pass


@pytest.mark.vcr
def test_create_and_save_api_key(
    hostname,
    mock_webbrowser,
    mock_handle_request,
    fake_auth_server,
    fake_auth_server_api_key,
):
    """
    The API key is created and saved to the keyring.
    """
    token = auth.login()
    assert token == auth.get_credentials()

    api_key = auth.create_and_save_api_key()
    assert api_key == auth.get_api_key()


@pytest.mark.vcr
def test_login(hostname, mock_webbrowser, mock_handle_request, fake_auth_server):
    """
    A token is returned for a successful login and this token can be retrieved
    via the get_token function.
    """
    token = auth.login()
    assert token == auth.get_credentials()


@pytest.mark.vcr
def test_login_failed(hostname, mock_webbrowser, mock_handle_request, fake_auth_server):
    """
    An AuthError exception is raised if the user's credentials are wrong.
    """
    token = auth.get_credentials_from_platform("bogus-flow-id")
    assert token is None


@pytest.mark.vcr
def test_get_token(hostname, mock_webbrowser, mock_handle_request, fake_auth_server):
    """
    If not logged in, get_token returns None. Once logged in, the expected
    token is returned.
    """
    auth.logout()
    assert auth.get_credentials() is None
    token = auth.login()

    assert token == auth.get_credentials()


@pytest.mark.vcr
def test_logout(hostname, mock_webbrowser, mock_handle_request, fake_auth_server):
    """
    After logging in, calling logout deletes the token from the keyring.
    """
    # Context setup to log in.
    token = auth.login()
    assert token == auth.get_credentials()

    # Logout
    auth.logout()
    assert auth.get_credentials() is None


def test_get_hostname_from_keyring(hostname):
    """
    If a hostname is set in the keyring, it is returned by get_host.
    """
    keyring.set_password(auth.KEYRING_APP_NAME, "hostname", hostname)
    assert auth.get_hostname() == hostname


def test_set_hostname(hostname):
    """
    The set_host function stores the hostname to the keyring.
    """
    # default context: no host set on keyring.
    assert keyring.get_password(auth.KEYRING_APP_NAME, "hostname") is None
    auth.set_hostname(hostname)
    # Now the host is in the keyring.
    assert keyring.get_password(auth.KEYRING_APP_NAME, "hostname") == hostname


def test_get_prefix_from_keyring(hostname):
    """
    If a prefix is set in the keyring, it is returned by get_prefix.
    """
    prefix = "/foo/bar"
    keyring.set_password(auth.KEYRING_APP_NAME, "prefix", prefix)
    assert auth.get_prefix() == prefix


def test_set_prefix(hostname):
    """
    The set_prefix function stores the prefix to the keyring.
    """
    # default context: no prefix set on keyring.
    assert keyring.get_password(auth.KEYRING_APP_NAME, "prefix") is None
    prefix = "/foo/bar"
    auth.set_prefix(prefix)
    # Now the host is in the keyring.
    assert keyring.get_password(auth.KEYRING_APP_NAME, "prefix") == prefix

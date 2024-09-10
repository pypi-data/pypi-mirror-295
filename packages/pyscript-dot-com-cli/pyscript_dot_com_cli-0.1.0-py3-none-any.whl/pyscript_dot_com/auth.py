"""
Authentication utilities.
"""

import json
import platform
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import keyring

if platform.system() == "Linux":
    from keyrings.cryptfile.cryptfile import CryptFileKeyring

    uname = platform.uname()
    keyring_password = f"{uname.node}_{uname.system}_{uname.machine}"

    kr = CryptFileKeyring()
    kr.keyring_key = keyring_password
    keyring.set_keyring(kr)

import requests

from .config import settings

__all__ = [
    "AuthError",
    "login",
    "get_credentials",
    "logout",
    "get_hostname",
    "set_hostname",
    "get_prefix",
    "set_prefix",
]


KEYRING_APP_NAME = "pyscript_dot_com"


class AuthError(Exception):
    """
    Raised when the user is unable to log in to the API.
    """

    pass


CLI_LOGIN_SUCCESSFUL = """
<html>
  <body>
    Login successful! Please return to your terminal and make history!
  </body>
</html>
"""


def create_and_save_api_key() -> str:
    """
    Uses the authenticated user to create an API key and stores it in the keyring.
    """
    api_key = _create_api_token()
    set_api_key(api_key)
    return api_key


def set_api_key(api_key: str):
    """
    Sets an API key in the keyring
    (also replaces if an existing one is present)
    """
    _delete_api_key()
    _store_api_key(api_key)


def get_api_key():
    """
    Return the API key for the given hostname.
    Returns a false-y empty string if no API key is set
    (i.e. the user isn't logged in).
    """
    hostname = get_hostname()
    return keyring.get_password(KEYRING_APP_NAME, f"{hostname}-api_key")


def save_credentials(token: str):
    """
    Sets a token in the keyring (also replaces if an existing one is present)
    """
    _delete_credentials()
    _store_credentials(token)


def login() -> str:
    """
    Go through the process of logging the user in.
    """

    # We create a uuid to identify each login flow. When the user has logged in we
    # can then use the uuid to retrieve the user's actual auth token (a JWT).
    flow_id = uuid.uuid4()

    # Start a local webserver (on a random, available port) that the user can be
    # redirected to at the end of the authentication dance.
    httpd = HTTPServer(("localhost", 0), _LocalRequestHandler)

    # Start the authentication dance by opening hitting the auth login endpoint in a
    # webbrowser (which will do the Ory redirect etc.).
    webbrowser.open(_get_auth_login_url(flow_id, httpd.server_port))

    # Wait for the redirect request at the end of the authentication dance!
    httpd.handle_request()

    return get_credentials_from_platform(flow_id)


class _LocalRequestHandler(BaseHTTPRequestHandler):
    """Handle the redirect request at the end of the authentication dance.

    This redirect lets us know that user has authenticated successfully.

    """

    def do_GET(self):  # NOQA
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(CLI_LOGIN_SUCCESSFUL.encode("utf-8"))


def get_credentials_from_platform(flow_id: uuid.UUID):
    """
    Get the credentials associated with the flow id we sent via the browser URL.

    Return None if no such token exists.
    """

    cookie = _get_credentials_from_api(flow_id)
    if cookie is not None:
        save_credentials(cookie)
        cookie = json.loads(cookie)

    return cookie


def logout() -> None:
    """
    Log out of the referenced API instance (clear the token and api key).
    """
    _delete_credentials()
    _delete_api_key()


def get_credentials() -> dict[str, str]:
    """
    Return the token for the given hostname.
    Returns a false-y empty string if no token is set (i.e. the user isn't
    logged in).
    """
    hostname = get_hostname()
    token = keyring.get_password(KEYRING_APP_NAME, hostname)
    if token:
        token = json.loads(token)
    return token


def get_hostname() -> str:
    """
    Returns the hostname of the currently active PyScript API instance.
    """
    return keyring.get_password(KEYRING_APP_NAME, "hostname") or settings.api_host


def get_prefix() -> str:
    """
    Returns the prefix of the currently active PyScript API instance.

    E.g. the path for the root of the API after the hostname.
    """
    return keyring.get_password(KEYRING_APP_NAME, "prefix") or settings.api_prefix


def set_hostname(hostname: str) -> None:
    """
    Sets the hostname for the currently active PyScript API instance.
    """
    keyring.set_password(KEYRING_APP_NAME, "hostname", hostname)


def set_prefix(prefix: str) -> None:
    """
    Sets the prefix for the currently active PyScript API instance.
    """
    keyring.set_password(KEYRING_APP_NAME, "prefix", prefix)


# Internal #############################################################################


def _get_auth_login_url(flow_id: str, server_port: int):
    """Return the auth login URL.

    We pass the flow id and the webserver port number as a query parameter.

    """

    return f"{settings.api_host}/api/auth/login?flow_id={flow_id}:{server_port}"


def _get_credentials_from_api(flow_id: uuid.UUID) -> str:
    """
    Get the JWT token from the API at the specified hostname, for the
    referenced user.
    """

    url = f"{settings.api_host}/api/auth/get-flow-token"
    response = requests.get(
        url,
        params={
            "flow_id": str(flow_id),
        },
    )
    if response.status_code != 200:
        raise AuthError(f"{response.status_code} {response.content}")

    payload = response.json()

    return json.dumps({payload.get("name"): payload.get("token")})


def _store_api_key(api_key: str):
    """
    Safely store the API Key for the given hostname.
    """
    hostname = get_hostname()
    if api_key:
        keyring.set_password(KEYRING_APP_NAME, f"{hostname}-api_key", api_key)
    else:
        raise ValueError("Cannot set empty api key.")


def _delete_api_key():
    """
    Safely delete the API Key for the given hostname.
    """
    hostname = get_hostname()
    if keyring.get_password(KEYRING_APP_NAME, f"{hostname}-api_key"):
        keyring.delete_password(KEYRING_APP_NAME, f"{hostname}-api_key")


def _store_credentials(token: str):
    """
    Safely store the token for the given hostname.
    """
    hostname = get_hostname()
    if token:
        keyring.set_password(KEYRING_APP_NAME, hostname, token)
    else:
        raise ValueError("Cannot set empty token.")


def _delete_credentials():
    """
    Safely delete the token for the given hostname.
    """
    hostname = get_hostname()
    if keyring.get_password(KEYRING_APP_NAME, hostname):
        keyring.delete_password(KEYRING_APP_NAME, hostname)


def _create_api_token() -> str:
    """
    Uses the authenticated user to create an API key.
    """
    token = get_credentials()
    url = f"{settings.api_host}/api/accounts/api-keys"
    response = requests.post(
        url, cookies=token, json={"name": "PyScript-cli", "expiry": 0}
    )

    if response.status_code != 200:
        raise AuthError(f"{response.status_code} {response.content}")

    return response.json()["token"]

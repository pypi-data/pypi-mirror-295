# type: ignore
import functools
import logging
from collections.abc import Callable
from typing import Any

import json
import requests
from requests.exceptions import HTTPError

# from urllib3.util.retry import Retry
from mlx.config import CredentialsConfig, EndpointsConfig, config
from mlx.models.credentials import Credentials
import hashlib


class SessionManager:
    _instance: "SessionManager" = None

    credentials: Credentials

    def __new__(cls, credentials: Credentials = None):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.session = requests.Session()
            cls._instance.credentials = credentials or CredentialsConfig()

        return cls._instance

    # def _setup_session(self):
    #     retries = Retry(
    #         total=1, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504]
    #     )
    #     self.session.mount("http://", HTTPAdapter(max_retries=retries))
    #     self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def request(
        self,
        method,
        url,
        headers={},
        can_retry=True,
        exception: Exception = None,
        **kwargs,
    ) -> requests.Response:
        try:
            headers.update(
                {
                    "Authorization": f"Bearer {self.credentials.token}",
                    "Accept": "application/json",
                },
            )

            if method.lower() == "post":
                headers["Content-Type"] = "application/json"
            response = self.session.request(
                method, url, headers=headers, timeout=45, **kwargs
            )
            logging.info(f"{method} {url}: {response.status_code} {response.text}")
            response.raise_for_status()
            return response
        except HTTPError as e:
            # Catch the exc to get out of its scope; avoid nested exceptions
            exception = e
            if e.response.status_code in [401, 403] and can_retry:
                self._maybe_authenticate()
        if exception and not can_retry:
            raise exception
        return self.request(
            method=method, url=url, headers=headers, can_retry=False, **kwargs
        )

    def _maybe_authenticate(self):
        if not self.credentials.token:
            if self.credentials.email and self.credentials.password:
                login(self.credentials)
                assert self.credentials.token
                if not self.credentials.workspace_id:
                    # attempt retrieving the first
                    from mlx.api.workspace import WorkspaceApi

                    self.credentials.workspace_id = WorkspaceApi().list()[0][
                        "workspace_id"
                    ]
                return
        elif self.credentials.refresh_token:
            assert self.credentials.email
            from mlx.session import refresh_auth_token

            refresh_auth_token(self.credentials)
            return


def authenticated(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    decorator that wraps a function with a session manager
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(SessionManager(), *args, **kwargs)
        except HTTPError as e:
            logging.error(e.response.text)
            raise e

    return wrapper


def login(credentials: Credentials):
    payload = {
        "email": credentials.email,
        "password": hashlib.md5((credentials.password).encode()).hexdigest(),
    }
    response = requests.post(f"{config.multilogin}/user/signin", json=payload)
    response.raise_for_status()
    js = json.loads(response.text)
    if response.status_code == 200:
        credentials.token = js["data"]["token"]
        credentials.refresh_token = js["data"]["refresh_token"]
    return credentials


def refresh_auth_token(credentials: Credentials):  # type: ignore
    """
    Refreshes the JWT auth token given an email and refresh token.
    """

    assert credentials.workspace_id

    payload = {
        "email": credentials.email,
        "refresh_token": credentials.refresh_token,
        "workspace_id": credentials.workspace_id,
    }
    endpoints = EndpointsConfig()
    response = requests.post(
        f"{endpoints.multilogin}/user/refresh_token",
        json=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    js = json.loads(response.text)
    logging.debug(js)
    if token := js.get("data", {}).get("token", {}):
        # Update the response['data'] in the config
        credentials.token = token
    if refresh_token := js.get("data", {}).get("refresh_token", {}):
        credentials.refresh_token = refresh_token
    return credentials


__all__ = ["SessionManager", "authenticated", "login", "refresh_auth_token"]

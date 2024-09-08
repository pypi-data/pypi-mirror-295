from __future__ import annotations
import logging
from typing import TypedDict

from mlx.api import Api
from mlx.models.profile import Profile
from mlx.config import config


class ProfileApi(Api):
    def get(self, id: str | None = None):
        if not id:
            return self.status()
        endpoint = f"{config.multilogin}/profile/statuses/{id}"
        response = self.session.request("get", endpoint)
        response.raise_for_status()
        return response.json()

    def status(self, *args, **kwargs) -> ProfileStateResponse:
        """
        Get the status of all profiles.
        """
        endpoint = f"{config.launcher_v1}/profile/statuses"
        response = self.session.request("get", endpoint)
        return response.json()

    def start(self, id: str):
        """
        Start a profile by its ID.

        Args:
            id (str): The ID of the profile to start.
        """
        endpoint = f"{config.multilogin}/profile/start/{id}"
        response = self.session.request("get", endpoint)
        response.raise_for_status()
        return response.json()

    def stop_all(self, *types):
        """
        Stop all profiles of specified types.

        Args:
            types: The types of profiles to stop.
        """
        endpoint = f"{config.multilogin}/profile/stop_all"
        if types:
            # Convert to URL encoded params
            joined = ",".join(map(str, types))
            endpoint = f"{endpoint}?types={joined}"
        response = self.session.request("get", endpoint)
        response.raise_for_status()
        return response.json()

    def default(self, body: dict | Profile = {}):
        """
        Create a new profile with default settings.

        Args:
            body_ (dict | Profile): The profile data or Profile object.

        Returns:
            Profile: A new profile with defaults applied.
        """
        """
        Create a new profile on top of the defaults
        """
        body_ = body
        if isinstance(body, Profile):
            body_ = body.dict()

        logging.debug("Request launch with body: %s", body_)

        return Profile.with_defaults(body_)


class State(TypedDict):
    message: str
    status: str
    timestamp: int


class ActiveCounter(TypedDict):
    cloud: int
    local: int
    quick: int


class Data(TypedDict):
    active_counter: ActiveCounter
    states: dict[str, State]


class Status(TypedDict):
    error_code: str
    http_code: int
    message: str


class ProfileStateResponse(TypedDict):
    data: Data
    status: Status

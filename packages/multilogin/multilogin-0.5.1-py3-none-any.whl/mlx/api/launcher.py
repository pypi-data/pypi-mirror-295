from __future__ import annotations

import logging

from mlx.api import Api
from mlx.config import config
from mlx.models.profile import Profile

import time


class BrowserCoreApi(Api):
    def download(self, browser_type: str = "mimic", version: str = "128", wait=False):
        """
        Load the browser core.

        Args:
            browser_type (str): The type of browser to load (e.g., mimic, stealthfox).
            version (str): The version of the browser core to load.
            wait (bool, optional): Wait for the download to complete. Defaults to `false`.

        Returns:
            dict: The response from the API.
        """
        url = f"{str(config.launcher_v1)}/load_browser_core"
        params = {"browser_type": browser_type, "version": version}

        logging.debug("Loading browser core with params: %s", params)

        response = self.session.request("get", url, params=params)
        response.raise_for_status()

        if wait:
            logging.info(
                "Waiting for download to complete; this may take a few seconds"
            )

            def short_ver(_ver):
                return str(_ver).split(".")[0]

            def has_version(_ver, _data):
                for it in _data:
                    if (
                        it["type"] == browser_type
                        and it["is_latest"] == True
                        and any(short_ver(_ver) == _ver for x in it["versions"])
                    ):
                        return True
                return False

            condition = False
            retries = 0

            while not condition:
                retries += 1
                data = self.inspect()["data"]
                condition = has_version(version, data)
                if condition:
                    break
                if retries % 5 == 0:
                    logging.info(
                        "Still waiting for download to complete; elapsed: {} seconds".format(
                            retries
                        )
                    )

        return response.json()

    def inspect(self):
        """
        Inspect downloaded browser cores.

        Returns:
            dict: The response from the API.
        """
        url = f"{str(config.launcher_v1)}/loaded_browser_cores"

        logging.debug("Listing browser cores")

        response = self.session.request("get", url)
        response.raise_for_status()
        return response.json()


class LauncherApi(Api):
    core: BrowserCoreApi

    def version(self):
        """
        Get the agent's version
        """
        url = f"{str(config.launcher_v1)}/version"

        logging.info("Fetching API version from: %s", url)

        response = self.session.request("get", url)
        response.raise_for_status()
        return response.json()

    def quick(self, body: dict | Profile = {}):
        """
        Launch a quick profile.

        Args:
            body (dict | Profile): Profile JSON to launch. Will overlay on top of default values.

        Returns:
            Profile: The profile object.
        """
        url = f"{config.launcher_v2}/profile/quick"

        body = Profile.with_defaults(body)

        logging.debug("with_defaults: %s", body)

        response = self.session.request("post", url, json=body.dict())
        response.raise_for_status()
        return response.json()

    def ready(self, wait=180):
        """
        Block until the API is ready or timeout is reached.

        Params:
        wait: int = 180 - Timeout (in seconds) to wait for the API to become ready. Don't like waiting? Make it 0.
        """

        start_time = time.time()
        while time.time() - start_time < wait:
            ver = self.version()
            if str(ver["status"]["http_code"]) == "200":
                return "API is ready"
            time.sleep(1)

        raise TimeoutError("Launcher not ready after {} seconds".format(wait))

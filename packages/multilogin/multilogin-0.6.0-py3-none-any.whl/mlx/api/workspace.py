import json

from mlx.api import Api
from mlx.config import config


class WorkspaceApi(Api):
    def get(self, *args, **kwargs):
        """
        Retrieve a list of workspaces.
        """
        return self.list(*args, **kwargs)

    def list(self, *args, **kwargs):
        """
        List all available workspaces.
        """
        response = self.session.request(
            "get",
            f"{config.multilogin}/user/workspaces",
        )
        if response.status_code != 200:
            raise Exception(response.text)
        js = json.loads(response.text)
        return js["data"]["workspaces"]

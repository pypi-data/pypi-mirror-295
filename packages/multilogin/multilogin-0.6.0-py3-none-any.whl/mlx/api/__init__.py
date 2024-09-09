import logging
from mlx.config import Config, config
from mlx.session import SessionManager


class Api:
    """
    Base class for all API modules
    Implements the `authenticated` decorator on all functions
    """

    session: SessionManager

    config: Config

    def __init__(self, credentials=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = SessionManager(credentials=credentials)  # type: ignore

        self.config = config

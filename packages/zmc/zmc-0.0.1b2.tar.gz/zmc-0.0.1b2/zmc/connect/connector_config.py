"""Connector config class module."""

import os

from zmc.utils import singleton

__all__ = ["config"]


@singleton
class ConnectorConfig:
    """Config class used within the connector context.

    The config reads values from the os environment and provides defaults if the
    env variables are not available. The config looks for two values:
        - ZMC_GUI_ID: (default 'gui-id') id of the gui that the script should
            connect to.
        - ZMC_PORT: (default 8766) the port a server should be serving and
            listening to.
    """

    def __init__(self):
        self.gui_id = os.getenv("ZMC_GUI_ID", "gui-id")
        self.port = int(os.getenv("ZMC_PORT", "8766"))


config = ConnectorConfig()

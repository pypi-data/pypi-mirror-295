"""Mock server module class."""

import logging

from .connector import Connector


__all__ = ["MockConnector"]


class MockConnector(Connector):
    """Mock connector, started on a separate thread."""

    def __init__(self, gui_id):
        super().__init__()
        self.gui_id = gui_id
        self._logger = logging.getLogger(__name__)

    async def _send_component_data(self, component):
        self._logger.debug(
            "Sending data to gui '%s' and component '%s'",
            self.gui_id,
            component.id,
        )
        # TODO: Consider nicer way of logging this?
        self._logger.debug("data: %s", component.data)

    async def _start_connector(self):
        self.is_connected = True
        self._logger.debug("starting mock connector")

    async def _stop_connector(self):
        """Stops the mock 'connector'."""
        self._logger.debug("stopping mock connector")

"""Abstract connector class module."""

from abc import ABC, abstractmethod


# TODO: move a large portion of the logic here. I think the majority of the
#       separate thread stuff can be moved here. Same goes for connection ready
#       logic.
class Connector(ABC):
    """Class that allows starting and stopping a server on a separate thread."""

    @abstractmethod
    def is_connected(self):
        """Indicates whether the connection has been established."""

    @abstractmethod
    def send_component_data(self, component, require_connection=False):
        """Send component data over to the mission control app."""

    @abstractmethod
    def start_connector_thread(self):
        """Start the server on a new separate thread."""

    @abstractmethod
    def stop_connector_thread(self):
        """Stop the server and the thread that it is running."""

    @abstractmethod
    def wait_for_connection(self, timeout=None):
        """Wait for the first client connection (with an optional timeout)."""

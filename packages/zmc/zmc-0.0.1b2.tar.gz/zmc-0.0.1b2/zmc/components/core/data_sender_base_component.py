"""BaseComponentValueSender class module."""

from abc import abstractmethod


from .base_component import BaseComponent

__all__ = ["DataSenderBaseComponent"]

# User friendly error message regarding the fact that the user attempted to send
# data outside a server context.
DATA_SENT_OUTSIDE_OF_CONTEXT_ERROR = (
    "Attempted to send data to Mission Control app outside of the "
    "`zmc.connect()` context which is not possible. Make sure to run your code "
    "inside of a `with zmc.connect():` context scope or run it in a function "
    "that has been decorated with `@zmc.connect()`."
)


class DataSenderBaseComponent(BaseComponent):
    """Base class for any component that will send data."""

    @property
    @abstractmethod
    def data(self):
        """Data corresponding to component.

        This function should be called in a separate thread so that whatever
        preprocessing is needed does not block calls or affect timing of the
        user's code.
        """

    def _send_data(self):
        # pylint:disable=import-outside-toplevel
        from zmc.connect.connector_context import context_connector

        server = context_connector.get()
        if server is None:
            raise RuntimeError(DATA_SENT_OUTSIDE_OF_CONTEXT_ERROR)
        server.send_component_data(self)

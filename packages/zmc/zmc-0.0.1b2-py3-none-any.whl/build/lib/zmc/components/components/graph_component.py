"""GraphComponent class module."""

from ..component_instance_registry import ComponentInstanceRegistry
from ..data_sender_base_component import DataSenderBaseComponent


__all__ = ["GraphComponent"]


@ComponentInstanceRegistry
class GraphComponent(DataSenderBaseComponent):
    """Graph component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._x = []
        self._y = []

    @property
    def data(self):
        return {
            "lines": [
                {
                    "x": list(self._x),
                    "y": list(self._y),
                }
            ]
        }

    def append_data(self, x, y):
        """Add a x, y pair to the graph and send data via server."""
        self._x.append(x)
        self._y.append(y)
        self._send_data()

    def plot(self, x, y):
        """Replace graph data entirely and send it."""
        self._x = x
        self._y = y
        self._send_data()

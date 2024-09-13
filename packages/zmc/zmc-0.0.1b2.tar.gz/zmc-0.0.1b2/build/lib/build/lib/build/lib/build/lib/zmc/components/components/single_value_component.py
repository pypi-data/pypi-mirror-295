"""SingleValueComponent class module."""

from ..value_receiver_base_component import ValueReceiverBaseComponent


__all__ = ["SingleValueComponent"]


class SingleValueComponent(ValueReceiverBaseComponent):
    """Receiver class which contains a single value."""

    def __init__(self, component_id, default_value):
        super().__init__(component_id)
        self.__value = default_value

    @property
    def value(self):
        """Value stored by the class."""
        return self.__value

    def _set_value(self, value):
        self.__value = value["value"]

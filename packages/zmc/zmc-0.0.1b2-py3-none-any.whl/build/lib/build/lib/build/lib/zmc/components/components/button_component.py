"""ButtonComponent class module."""

from ..component_instance_registry import ComponentInstanceRegistry
from ..value_receiver_base_component import ValueReceiverBaseComponent


__all__ = ["ButtonComponent"]


@ComponentInstanceRegistry
class ButtonComponent(ValueReceiverBaseComponent):
    """Button class that calls a function whenever it is clicked."""

    def _set_value(self, _):
        pass  # No value but this is still needed to make the class concrete.

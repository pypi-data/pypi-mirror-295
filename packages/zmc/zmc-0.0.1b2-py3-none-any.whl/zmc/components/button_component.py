"""ButtonComponent class module."""

from .core import ValueReceiverBaseComponent


__all__ = ["Button"]


class Button(ValueReceiverBaseComponent):
    """Button class that calls a function whenever it is clicked."""

    # No value but this is still needed to make the class concrete.
    def _set_value(self, _):
        """No value is set for buttons"""

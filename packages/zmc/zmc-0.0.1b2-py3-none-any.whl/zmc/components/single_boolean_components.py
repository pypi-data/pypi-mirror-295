"""SingleBooleanComponent class module."""

from .core import SingleValueComponent


__all__ = ["Toggle"]


class SingleBooleanComponent(SingleValueComponent):
    """Boolean receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, False)


class Toggle(SingleBooleanComponent):
    """Toggle class containing a single boolean value.

    The class has a single boolean value that can be accessed as an attribute:
    `toggle.value`.
    """

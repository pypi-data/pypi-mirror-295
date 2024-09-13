"""SingleTextComponent class module."""

from .core import SingleValueComponent


__all__ = ["TextInput"]


class SingleTextComponent(SingleValueComponent):
    """Text receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, "")


class TextInput(SingleTextComponent):
    """Text class, representing a freeform or dropdown text component.

    The class has a single value that can be accessed as an attribute:
    `text_input.value`.
    """

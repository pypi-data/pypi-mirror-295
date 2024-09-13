"""SingleNumberComponent class module."""

from .core import SingleValueComponent


__all__ = ["Slider", "NumericInput"]


class SingleNumberComponent(SingleValueComponent):
    """Number receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, 1)


class Slider(SingleNumberComponent):
    """Slider class which contains a single value.

    A slider has a value of a single number that can be accessed as an
    attribute: `slider.value`.
    """


class NumericInput(SingleNumberComponent):
    """Numeric class, representing a freeform or dropdown number component.

    The class has a single value that can be accessed as an attribute:
    `numeric_input.value`.
    """

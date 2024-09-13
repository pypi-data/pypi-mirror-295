"""SingleNumberComponent class module."""

from .single_value_component import SingleValueComponent


__all__ = ["SingleNumberComponent"]


class SingleNumberComponent(SingleValueComponent):
    """Number receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, 1)

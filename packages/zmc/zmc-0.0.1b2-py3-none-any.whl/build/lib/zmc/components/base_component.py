"""BaseComponent class module."""

from abc import ABC

__all__ = ["BaseComponent"]


# pylint: disable=too-few-public-methods
class BaseComponent(ABC):
    """Base class for all components.

    The base component class simply contains a unique id that can be accessed as
    a property.
    """

    def __init__(self, component_id):
        if not isinstance(component_id, str) or component_id == "":
            raise ValueError(
                "Component id must be a non empty string, given:", component_id
            )
        self.__id = component_id

    @property
    def id(self) -> str:
        """Unique identifier for component."""
        return self.__id

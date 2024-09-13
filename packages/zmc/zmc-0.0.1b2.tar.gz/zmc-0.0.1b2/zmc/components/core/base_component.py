"""BaseComponent class module."""

from abc import ABCMeta

from zmc.utils import InstanceRegistry

__all__ = ["BaseComponent"]


class _BaseComponentMeta(ABCMeta):
    """Metaclass for BaseComponent class which contains an instance registry."""

    __REGISTRY = InstanceRegistry()

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

    @property
    def registry(cls):
        """Get the instance registry dict for the BaseComponent class"""
        return _BaseComponentMeta.__REGISTRY.get_dict()

    def __call__(cls, *args, **kwds):
        instance = super().__call__(*args, **kwds)
        _BaseComponentMeta.__REGISTRY.register(instance)
        return instance


class BaseComponent(metaclass=_BaseComponentMeta):
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

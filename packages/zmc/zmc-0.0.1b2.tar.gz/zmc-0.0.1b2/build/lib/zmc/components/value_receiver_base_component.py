"""BaseComponentValueSetter class module."""

import inspect

from abc import abstractmethod

from .base_component import BaseComponent


__all__ = ["ValueReceiverBaseComponent"]


# TODO: implement `remove_callback`
# TODO: factor out into Callback function? might even already exist in py
# TODO: pass in a value as one of the arguments?
class ValueReceiverBaseComponent(BaseComponent):
    """Base class for any component that can set a value.

    Any concrete subclass must implement _set_value(self, value).
    """

    def __init__(self, component_id):
        super().__init__(component_id)
        self._func = None
        self._func_args = []
        self._func_kwargs = {}

    def set_callback(self, func, *args, **kwargs):
        """Sets a callback function that will be called when value is received.

        Any arguments passed in after the callback function will be passed to
        the function when it is called.
        """
        if not inspect.isroutine(func):
            raise ValueError(f"`func` must be a callable function, given: {func}")

        self._func = func
        self._func_args = args
        self._func_kwargs = kwargs

    @abstractmethod
    def _set_value(self, value):
        """Store the value pass in for future access."""

    def receive_value(self, value):
        """Receive the value sent from the Mission Control app.

        First sets the value on the component. Once that is done, calls any
        callback functions that have been added.

        Args:
            value: component value that has been received.
        """
        self._set_value(value)
        if self._func:
            self._func(*self._func_args, **self._func_kwargs)

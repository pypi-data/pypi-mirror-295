import pytest

from .base_component import BaseComponent
from .value_receiver_base_component import ValueReceiverBaseComponent


# TODO: add tests for callbacks


def test_is_base_subclass():
    assert issubclass(ValueReceiverBaseComponent, BaseComponent)


def test_is_abstract():
    with pytest.raises(TypeError, match="abstract class"):
        # pylint:disable=abstract-class-instantiated
        ValueReceiverBaseComponent("id")


def test_impl():
    class Component(ValueReceiverBaseComponent):
        def _set_value(self, value):
            self.value = value

    c = Component("id")
    value = 9
    c.receive_value(value)
    assert c.value == value

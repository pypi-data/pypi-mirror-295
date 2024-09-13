"""SingleBooleanComponent class module."""

from .core import BaseComponent
from .core import SingleValueComponent

from .single_text_components import TextInput, SingleTextComponent


def test_is_single_value_subclass():
    assert issubclass(SingleTextComponent, SingleValueComponent)


def test_default_value():
    c = SingleTextComponent("id")

    assert c.value == ""


def test_subclasses():
    assert issubclass(TextInput, SingleTextComponent)


def test_gets_registered():
    cid = "id"
    c = TextInput(cid)
    assert BaseComponent.registry.get(cid) == c

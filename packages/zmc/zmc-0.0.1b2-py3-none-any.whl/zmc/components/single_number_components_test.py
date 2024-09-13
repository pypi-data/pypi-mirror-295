"""SingleBooleanComponent class module."""

from .core import BaseComponent
from .core import SingleValueComponent

from .single_number_components import (
    NumericInput,
    SingleNumberComponent,
    Slider,
)


def test_is_single_value_subclass():
    assert issubclass(SingleNumberComponent, SingleValueComponent)


def test_default_value():
    c = SingleNumberComponent("id")

    assert c.value == 1


def test_subclasses():
    assert issubclass(Slider, SingleNumberComponent)
    assert issubclass(NumericInput, SingleNumberComponent)


def test_gets_registered():
    id1 = "id1"
    id2 = "id2"
    c1 = Slider(id1)
    assert BaseComponent.registry.get(id1) == c1
    c2 = NumericInput(id2)
    assert BaseComponent.registry.get(id2) == c2

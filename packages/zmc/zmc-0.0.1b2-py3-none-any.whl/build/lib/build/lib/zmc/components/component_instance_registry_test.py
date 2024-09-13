import pytest

from .base_component import BaseComponent
from .component_instance_registry import ComponentInstanceRegistry


@ComponentInstanceRegistry
class Component(BaseComponent):
    def __init__(self, component_id, value=None):
        super().__init__(component_id)
        self.value = value

    def get_value(self):
        return self.value


@pytest.fixture(autouse=True, scope="function")
def clear_registry():
    ComponentInstanceRegistry.clear_registry()


def test_instance_type_is_preserved():
    c1 = Component("id1")

    assert isinstance(c1, Component)
    assert isinstance(c1, BaseComponent)


def test_class_type_is_preserved():
    assert issubclass(Component, BaseComponent)
    assert not issubclass(Component, ComponentInstanceRegistry)


def test_instance_gets_registered():
    id1 = "id1"
    id2 = "id2"
    c1 = Component(id1)
    c2 = Component(id2)

    assert ComponentInstanceRegistry.get_instance(id1) == c1
    assert ComponentInstanceRegistry.get_instance(id2) == c2
    assert ComponentInstanceRegistry.get_instance("not registered id") is None


def test_non_unique_id_raises():
    cid = "id1"
    Component(cid)
    with pytest.raises(ValueError, match="already.*instantiated with id.*" + cid):
        Component(cid)


def test_decorate_non_component_subclass_raises():
    with pytest.raises(
        ValueError, match="can only decorate subclasses of BaseComponent"
    ):

        @ComponentInstanceRegistry
        class BadComponent:
            pass


def test_instance_initialization_preserved():
    value = 6  # arbitrary value
    c1 = Component("id", value)

    assert c1.get_value() == value

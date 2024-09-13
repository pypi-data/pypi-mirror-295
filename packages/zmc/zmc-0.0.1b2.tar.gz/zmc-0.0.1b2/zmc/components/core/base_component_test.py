import pytest

from .base_component import BaseComponent


class Component(BaseComponent):
    pass


class Component2(BaseComponent):
    pass


class ComponentWithError(BaseComponent):
    def __init__(self, instance_id):
        super().__init__(instance_id)
        raise RuntimeError("Oh no!")


def test_id_available():
    cid = "id1"
    c1 = Component(cid)

    assert c1.id is cid


def test_invalid_id_raises():
    with pytest.raises(
        ValueError, match=f"Component id must be a non empty string.*{None}"
    ):
        Component(None)
    with pytest.raises(
        ValueError, match=f"Component id must be a non empty string.*{9}"
    ):
        Component(9)
    with pytest.raises(
        ValueError, match="Component id must be a non empty string.*"
    ):
        Component("")


def test_registry():
    id1 = "id1"
    id2 = "id2"
    c1 = Component(id1)
    c2 = Component(id2)

    assert BaseComponent.registry == {id1: c1, id2: c2}


def test_without_super_init_call():
    class ComponentWithoutSuperInit1(BaseComponent):
        """A very hacky class that does not call the super __init__ method.

        For testing purposes, the class has a valid `self.id` so that it can be
        registered.
        """

        # pylint: disable=super-init-not-called
        def __init__(self, instance_id):
            # pylint: disable=invalid-name
            self._BaseComponent__id = instance_id

    cid = "id"
    c = ComponentWithoutSuperInit1(cid)
    assert BaseComponent.registry.get(cid) == c

    class ComponentWithoutSuperInit2(BaseComponent):
        """A class that does not call the super __init__ method."""

        # pylint: disable=super-init-not-called
        def __init__(self):
            pass

    with pytest.raises(AttributeError):
        ComponentWithoutSuperInit2()


def test_error_in_init_does_not_register():
    cid = "id"
    with pytest.raises(RuntimeError):
        ComponentWithError(cid)

    assert cid not in BaseComponent.registry


def test_non_unique_id_raises():
    cid = "id1"
    Component(cid)
    # Instance from same class and same id, raises
    with pytest.raises(
        ValueError, match="already.*instance with the same id.*" + cid
    ):
        Component(cid)
    # Instance from different subclass and same id, raises
    with pytest.raises(
        ValueError, match="already.*instance with the same id.*" + cid
    ):
        Component2(cid)

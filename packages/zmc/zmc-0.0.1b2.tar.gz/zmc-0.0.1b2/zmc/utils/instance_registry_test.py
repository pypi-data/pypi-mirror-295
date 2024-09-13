import pytest

from .instance_registry import InstanceRegistry


class ClassWithId:
    def __init__(self, instance_id):
        self.id = instance_id


class ClassWithName:
    def __init__(self, name):
        self.name = name


def test_registering_instances():
    registry = InstanceRegistry()
    id1 = "id1"
    id2 = "id2"
    c1 = ClassWithId(id1)
    c2 = ClassWithId(id2)
    registry.register(c1)
    registry.register(c2)

    assert registry.get_instance(id1) == c1
    assert registry.get_instance(id2) == c2
    assert registry.get_instance("not registered id") is None
    assert len(registry) == 2


def test_custom_id_fn():
    registry = InstanceRegistry(id_fn=lambda x: x.name)
    name = "name"
    id1 = "id"
    c1 = ClassWithName(name)
    registry.register(c1)

    assert registry.get_instance(id1) is None
    assert registry.get_instance(name) == c1


def test_deregistering_instance():
    registry = InstanceRegistry()
    id1 = "id1"
    c1 = ClassWithId(id1)
    registry.register(c1)
    assert registry.get_instance(id1) == c1

    registry.deregister(id1)
    assert registry.get_instance(id1) is None


def test_clear_registry():
    registry = InstanceRegistry()
    id1 = "id1"
    id2 = "id2"
    c1 = ClassWithId(id1)
    c2 = ClassWithId(id2)
    registry.register(c1)
    registry.register(c2)
    assert registry.get_instance(id1) == c1
    assert registry.get_instance(id2) == c2

    registry.clear()
    assert len(registry) == 0


def test_get_dict():
    registry = InstanceRegistry()
    id1 = "id1"
    id2 = "id2"
    c1 = ClassWithId(id1)
    c2 = ClassWithId(id2)
    registry.register(c1)
    registry.register(c2)
    assert registry.get_dict() == {id1: c1, id2: c2}


def test_asserting_type():
    registry = InstanceRegistry(instance_type=ClassWithId)
    id1 = "id1"
    name2 = "name2"
    c1 = ClassWithId(id1)
    c2 = ClassWithName(name2)
    registry.register(c1)
    with pytest.raises(
        ValueError,
        match=f"Expected.*instance of.*{ClassWithId}.*given.*{ClassWithName}",
    ):
        registry.register(c2)


def test_non_unique_id_raises():
    registry = InstanceRegistry()
    cid = "id1"
    c1 = ClassWithId(cid)
    registry.register(c1)
    c2 = ClassWithId(cid)
    with pytest.raises(
        ValueError, match="already.*instance with the same id.*" + cid
    ):
        registry.register(c2)


def test_no_positional_args():
    with pytest.raises(TypeError):
        # pylint: disable=too-many-function-args
        InstanceRegistry(lambda x: x.name)

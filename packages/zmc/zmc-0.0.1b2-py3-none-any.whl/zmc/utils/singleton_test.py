import pytest

from .singleton import singleton


# pylint: disable=invalid-name
@pytest.fixture(scope="function")
def TestSingletonClass():

    @singleton
    class NewSingletonClass:
        def __init__(self, value):
            self.value = value

    yield NewSingletonClass


def test_singleton_instance(TestSingletonClass):
    obj1 = TestSingletonClass(1)
    obj2 = TestSingletonClass(1)

    assert obj1 is obj2  # Both objects should be the same instance


def test_singleton_init_only_called_once(TestSingletonClass):
    obj1 = TestSingletonClass(10)
    obj2 = TestSingletonClass(20)

    assert obj1 is obj2  # Both objects should be the same instance

    # value should not have been updated from first instantiation
    assert obj1.value == 10
    assert obj2.value == 10


def test_singleton_second_call_ignores_args(TestSingletonClass):
    obj1 = TestSingletonClass(10)
    obj2 = TestSingletonClass()
    obj3 = TestSingletonClass(1, 2, 3)

    assert obj1 is obj2
    assert obj1 is obj3

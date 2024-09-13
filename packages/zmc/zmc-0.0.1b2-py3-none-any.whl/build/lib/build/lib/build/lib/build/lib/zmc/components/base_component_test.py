import pytest

from .base_component import BaseComponent


class Component(BaseComponent):
    pass


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
    with pytest.raises(ValueError, match="Component id must be a non empty string.*"):
        Component("")

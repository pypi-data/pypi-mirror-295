import pytest

from .core import _BaseComponentMeta


@pytest.fixture(autouse=True, scope="function")
def clear_base_component_class_registry():
    # The BaseComponent registry should already be empty but, just in case, we
    # clear both before and after the test is run.
    _BaseComponentMeta._BaseComponentMeta__REGISTRY.clear()
    yield
    _BaseComponentMeta._BaseComponentMeta__REGISTRY.clear()

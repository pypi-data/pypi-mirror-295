import re
import pytest

from zmc.connect.connector_context import context_connector

from .base_component import BaseComponent
from .data_sender_base_component import (
    DataSenderBaseComponent,
    DATA_SENT_OUTSIDE_OF_CONTEXT_ERROR,
)


class Component(DataSenderBaseComponent):

    def __init__(self, component_id):
        super().__init__(component_id)
        self._data = "dummy data"

    @property
    def data(self):
        return self._data  # pragma: no cover

    def send_data(self):
        self._send_data()


@pytest.fixture
def mock_context_server(mocker):
    mock_instance = mocker.Mock()

    token = context_connector.set(mock_instance)
    yield mock_instance
    context_connector.reset(token)


def test_is_base_subclass():
    assert issubclass(DataSenderBaseComponent, BaseComponent)


def test_is_abstract():
    with pytest.raises(TypeError, match="abstract class"):
        # pylint:disable=abstract-class-instantiated
        DataSenderBaseComponent("id")


def test_outside_of_context_raises():
    c = Component("id")

    with pytest.raises(
        RuntimeError, match=re.escape(DATA_SENT_OUTSIDE_OF_CONTEXT_ERROR)
    ):
        c.send_data()


def test_inside_context_calls_send(mock_context_server):
    component_id = "id"
    c = Component(component_id)
    c.send_data()

    mock_context_server.send_component_data.assert_called_once()
    mock_context_server.send_component_data.assert_called_once_with(c)

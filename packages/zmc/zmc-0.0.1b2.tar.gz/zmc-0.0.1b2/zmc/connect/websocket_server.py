"""WebsocketServer class module."""

import asyncio
import json
import websockets

from zmc.components.core import BaseComponent
from zmc.components.core import ValueReceiverBaseComponent
from zmc.version import __version__

from .async_utils import cancellable, async_repeat
from .connector import Connector


__all__ = ["WebSocketServer"]


# User friendly error message regarding the fact that a component that does not
# allow for setting a value was sent a value from the Mission Control app.
SETTING_VALUE_ON_NON_SETTER_ERROR_TEMPLATE = (
    "Component id, '{}', was attached to a component that does not expect to "
    "receive any values. However, the Mission Control app is sending values to "
    "the component with this id.\nPlease verify that you are using the right "
    "id when initializing this component."
)

# Rate (in Hz) at which messages will be sent over websockets.
_THROTTLE_RATE = 61


class WebSocketServer(Connector):
    """Server that allows caller to open up a websocket on a separate thread.

    Args:
        - host: host as per similarly named asyncio.serve() function parameter
        - port: port as per similarly named asyncio.serve() function parameter
        - gui_id: id of the gui this server is going to connect to.
    """

    def __init__(self, host, port, gui_id):
        super().__init__()
        self.host = host
        self.port = port
        self.gui_id = gui_id

        # Server/websocket related attributes
        self.__server = None
        self.__websockets = set()

        # Queued data related attirbutes
        self.__data_component_queue = asyncio.Queue()
        self.__send_queued_data_task = None

    def _reset(self):
        self.__server = None
        self.__websockets.clear()
        self.__data_component_queue = asyncio.Queue()
        self.__send_queued_data_task = None

    @cancellable
    async def _send_all_component_data(self, components):
        data_event = {
            "type": "send-all-data",
            "guiId": self.gui_id,
            "components": [
                {
                    "componentId": component.id,
                    "data": component.data,
                }
                for component in components.values()
            ],
            "pyVersion": __version__,
        }
        json_data_event = json.dumps(data_event)
        websockets_set = self.__websockets.copy()
        for websocket in websockets_set:
            try:
                await websocket.send(json_data_event)
            except websockets.ConnectionClosed:
                pass

    @cancellable
    @async_repeat(1 / _THROTTLE_RATE)
    async def _send_queued_component_data(self):
        items = {}
        while not self.__data_component_queue.empty():
            component = await self.__data_component_queue.get()
            items[component.id] = component
        if items:
            await self._send_all_component_data(items)

    async def _start_send_queued_data_task(self):
        if (
            self.__send_queued_data_task is None
            or self.__send_queued_data_task.done()
        ):
            self.__send_queued_data_task = asyncio.create_task(
                self._send_queued_component_data()
            )

    async def _send_component_data(self, component):
        """Queues up component data to be sent."""
        # Add component data to the queue
        await self.__data_component_queue.put(component)
        # Start the queued data sending loop if it hasn't been already.
        await self._start_send_queued_data_task()

    # TODO: should refactor this to be a little more palettable
    async def _websocket_consumer(self, websocket):
        async for message in websocket:
            event = json.loads(message)
            # TODO: handle app versions (for future proofing as things change)
            _app_version = event["app_version"]
            if event["type"] == "set-value":
                component_id = event["component_id"]
                component = BaseComponent.registry.get(component_id, None)
                if component is None:
                    continue  # Didn't find component. Do nothing and skip.
                if not isinstance(component, ValueReceiverBaseComponent):
                    raise ValueError(
                        SETTING_VALUE_ON_NON_SETTER_ERROR_TEMPLATE.format(
                            component.id
                        )
                    )
                component.receive_value(event.get("value", None))
            if event["type"] == "initialize":
                components = event["components"]
                for component_json in components:
                    component_id = component_json["component_id"]
                    component = BaseComponent.registry.get(component_id, None)
                    if component is None:
                        continue  # Didn't find component. Do nothing and skip.
                    value = component_json.get("value", None)
                    if not value:
                        continue  # No value to update.
                    if not isinstance(component, ValueReceiverBaseComponent):
                        raise ValueError(
                            SETTING_VALUE_ON_NON_SETTER_ERROR_TEMPLATE.format(
                                component.id
                            )
                        )
                    component.receive_value(value)
                self.is_connected = True  # Signal that a connection is ready
            if event["type"] == "kill-func":
                self._exit_original_thread()

    async def _websocket_handler(self, websocket, _):
        self.__websockets.add(websocket)
        consumer_task = asyncio.create_task(self._websocket_consumer(websocket))

        done, pending = await asyncio.wait(
            [consumer_task], return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        self.__websockets.discard(websocket)
        if not self.__websockets and self.is_connected:
            # If there are no websockets left, then there is no connection.
            self.is_connected = False

        for task in done:
            try:
                error = task.exception()
                if error is not None:
                    self._handle_thread_exception(error)
            except asyncio.CancelledError:
                pass

    async def _start_connector(self):
        self.__server = await websockets.serve(
            self._websocket_handler, self.host, self.port
        )

    async def _stop_connector(self):
        if self.__server is not None and self.__server.is_serving():
            self.__server.close()
            await self.__server.wait_closed()

        self._reset()

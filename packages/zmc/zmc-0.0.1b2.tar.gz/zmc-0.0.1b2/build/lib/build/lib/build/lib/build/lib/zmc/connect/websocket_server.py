"""WebsocketServer class module."""

import asyncio
import ctypes
import json
import sys
import threading
import traceback
import websockets

from ..components.value_receiver_base_component import ValueReceiverBaseComponent
from ..components.component_instance_registry import ComponentInstanceRegistry
from ..version import __version__

from .async_utils import cancellable, cancel_loop_tasks, async_repeat
from .connector import Connector


__all__ = ["WebSocketServer"]


# TODO: This is not a very helpful message for users. It's good enough for now
#       but at some point we'll want to fix that (which component, id, and
#       details as to what is going on are unclear).
# User friendly error message regarding the fact that a component that does not
# allow for setting a value was given an idea that corresponds to a control in
# the Mission Control app.
SETTING_VALUE_ON_NON_SETTER_ERROR_MSG = (
    "Component id was attached to the wrong component. Specifically, it was "
    "set on a component that does not accept a value."
)

# Rate (in Hz) at which messages will be sent over websockets.
_THROTTLE_RATE = 61


# TODO: handle errors in handler?
# TODO: test interrupt logic (exit) on windows, then cleanup
class WebSocketServer(Connector):
    """Server that allows caller to open up a websocket on a separate thread.

    Args:
        - host: host as per similarly named asyncio.serve() function parameter
        - port: port as per similarly named asyncio.serve() function parameter
        - gui_id: id of the gui this server is going to connect to.
    """

    def __init__(self, host, port, gui_id):
        self.host = host
        self.port = port
        self.gui_id = gui_id
        self._clear()
        self._throttle_rate = 60

    def _clear(self):
        # Original caller related attributes
        self.__original_thread = None

        # Server related attributes
        self.__server = None
        self.__server_thread = None
        self.__server_loop = None

        # Connection related attributes
        self.__client_connected_event = threading.Event()
        self.__websockets = set()

        # Queued data related attirbutes
        self.__data_component_queue = asyncio.Queue()
        self.__send_queued_data_task = None

    def is_serving(self):
        """Indicates whether the server is currently up and running."""
        return self.__server is not None and self.__server.is_serving()

    def is_connected(self):
        """Indicates whether there is at least one websocket connection."""
        return self.is_serving() and self.__websockets

    async def _exit_original_thread(self):
        if self.__original_thread is None:
            return  # Nothing to do if we don't know which thread to exit.
        # TODO: test on windows, then cleanup
        # signal.pthread_kill(self.original_thread.ident, signal.SIGUSR1)
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.__original_thread.ident), ctypes.py_object(SystemExit)
        )

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
        if self.__send_queued_data_task is None or self.__send_queued_data_task.done():
            self.__send_queued_data_task = asyncio.create_task(
                self._send_queued_component_data()
            )

    async def _queue_component_data(self, component):
        await self.__data_component_queue.put(component)
        await self._start_send_queued_data_task()

    def send_component_data(self, component, require_connection=False):
        """Send data over to a given component.

        Args:
            - component: DataSenderComponent whose data will be sent over.
            - require_connection: (default: False) whether to raise an exception
                if there is no connection or to do nothing silently.

        Raises:
            RuntimeError: if require_connection is True and there are no
                connections at the time of being called.
        """
        if require_connection and not self.is_connected():
            raise RuntimeError("Not Connected!")
        asyncio.run_coroutine_threadsafe(
            self._queue_component_data(component), self.__server_loop
        )

    # TODO: should refactor this to be a little more palettable
    async def _websocket_consumer(self, websocket):
        async for message in websocket:
            event = json.loads(message)
            # TODO: handle app versions (for future proofing as things change)
            _app_version = event["app_version"]
            if event["type"] == "set-value":
                target_id = event["component_id"]
                component = ComponentInstanceRegistry.get_instance(target_id)
                if component is None:
                    continue  # Didn't find component. Do nothing and skip.
                if not isinstance(component, ValueReceiverBaseComponent):
                    raise ValueError(SETTING_VALUE_ON_NON_SETTER_ERROR_MSG)
                component.receive_value(event.get("value", None))
            if event["type"] == "initialize":
                components = event["components"]
                for component_json in components:
                    component_id = component_json["component_id"]
                    component = ComponentInstanceRegistry.get_instance(component_id)
                    if component is None:
                        continue  # Didn't find component. Do nothing and skip.
                    value = component_json.get("value", None)
                    if not value:
                        continue  # No value to update.
                    if not isinstance(component, ValueReceiverBaseComponent):
                        raise ValueError(SETTING_VALUE_ON_NON_SETTER_ERROR_MSG)
                    component.receive_value(value)
                self.__client_connected_event.set()  # Signal that a client is ready
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

        # TODO: handle errors? Not quite right. This throws an error and prints
        #       it but doesn't do anything else. We would need to propagate
        #       somehow or be happy with this behavior. Worth looking into more.
        for task in done:
            try:
                error = task.exception()
                if error is not None:
                    # For now, simply print out the error
                    traceback.print_exception(
                        type(error), error, error.__traceback__, file=sys.stdout
                    )
            except asyncio.CancelledError:
                pass

    @cancellable
    async def _run_server(self, server_ready_event):
        self.__server = await websockets.serve(
            self._websocket_handler, self.host, self.port
        )
        server_ready_event.set()  # Signal that the server is ready
        await self.__server.wait_closed()

    def _stop_server(self):
        if not self.is_serving():
            return  # Server is already not running so nothing to do.

        async def stop_server():
            self.__server.close()
            await self.__server.wait_closed()

        future = asyncio.run_coroutine_threadsafe(stop_server(), self.__server_loop)
        future.result()

    def _server_thread_fn(self, loop, server_ready_event):
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._run_server(server_ready_event))
        finally:
            loop.run_forever()

    def wait_for_connection(self, timeout=None):
        """Wait for the first client websocket connection to be made.

        Once a first connection has been made, this will return immediately
        for the rest of the time the server is up. This is true even if all of
        the connections have since been closed.

        Args:
            - timeout: (default None) The amount of time (in seconds) to wait
                before raising an error.

        Raises:
            TimeoutError: If timeout arg is set and the wait lasts for longer
                than the amount specified.
        """
        if not self.__client_connected_event.wait(timeout=timeout):
            raise TimeoutError("Timeout waiting for client connection")

    def start_connector_thread(self):
        """Start the websocket server on a new separate thread.

        The thread that the server was started from is stored so that it can be
        exited upon a request via the websocket. The function does not return
        until the server has fully been started.
        """
        self.__original_thread = threading.current_thread()

        # TODO: change this to interrupt the main thread?
        def handle_thread_exception(_loop, context):
            msg = context.get("exception", context["message"])
            print(f"Caught exception: {msg}")

        # Create a new event loop and start it in a new thread.
        self.__server_loop = asyncio.new_event_loop()
        self.__server_loop.set_exception_handler(handle_thread_exception)
        server_ready_event = threading.Event()
        self.__server_thread = threading.Thread(
            target=self._server_thread_fn,
            args=(self.__server_loop, server_ready_event),
        )
        self.__server_thread.start()

        # Wait until the server is ready before returning
        server_ready_event.wait()

    def _stop_thread(self, num_retries=None, timeout=0.1):
        if not self.__server_thread.is_alive():
            self.__server_loop.close()
            return  # Server thread has stopped and the loop is closed. Hooray!
        if num_retries < 0:
            raise RuntimeError("Unable to properly close connection thread.")
        cancel_loop_tasks(self.__server_loop)
        if self.__server_loop and self.__server_loop.is_running():
            self.__server_loop.call_soon_threadsafe(self.__server_loop.stop)
        self.__server_thread.join(timeout=timeout)  # wait for thread to cleanup.
        self._stop_thread(
            num_retries=num_retries - 1 if num_retries is not None else None,
            timeout=timeout,
        )

    def stop_connector_thread(self):
        """Stop the websocket server and the thread it was on.

        After stopping the server, all other tasks on the server thread loop are
        also canceled and then the thread itself is closed and the class
        instance is reset.
        """
        self._stop_server()
        self._stop_thread(num_retries=5)

        self._clear()

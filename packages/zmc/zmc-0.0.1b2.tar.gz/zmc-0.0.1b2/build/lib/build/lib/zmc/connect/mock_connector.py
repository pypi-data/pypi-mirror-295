"""Mock server module class."""

import asyncio
import threading

from .async_utils import cancel_loop_tasks
from .connector import Connector


__all__ = ["MockConnector"]


class MockConnector(Connector):
    """Mock server, started on a separate thread."""

    def __init__(self, gui_id, verbose=False):
        self.gui_id = gui_id
        self.verbose = verbose
        self._clear()

    def _clear(self):
        self.__connector_thread = None
        self.__connector_loop = None

        # Connection related attributes
        self.__client_connected_event = threading.Event()

    def is_connected(self):
        """Indicates whether the mock 'connection' is established."""
        return self.__connector_thread.is_alive() is not None

    async def _mock_send_data(self, component):
        if self.verbose:
            print("Sending data:")
            print("Gui id:", self.gui_id)
            print("Component id:", component.id)
            print("data:", component.data)

    def send_component_data(self, component, require_connection=False):
        """Mocks sending data.

        If verbose=True was set in class, prints out what it would send.

        Args:
            - component: ComponentDataSender whose data will be sent over.
            - require_connection: (default: False) whether to raise an exception
                if there is no connection or to do nothing silently.

        Raises:
            RuntimeError: if require_connection is True and there are no
                connections at the time of being called.
        """
        if require_connection and not self.is_connected():
            raise RuntimeError("Not Connected!")
        future = asyncio.run_coroutine_threadsafe(
            self._mock_send_data(component), self.__connector_loop
        )
        future.result()

    def _mock_server_thread_fn(self, loop):

        async def _mock_start_server():
            self.__client_connected_event.set()
            if self.verbose:
                print("starting mock connector")

        asyncio.set_event_loop(loop)
        loop.run_until_complete(_mock_start_server())
        loop.run_forever()

    def wait_for_connection(self, timeout=None):
        """Wait for the mock 'connection' to be ready.

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
        """Start a mock 'server' on a new thread. It does nothing."""
        # Create a new event loop and start it in a new thread.
        self.__connector_loop = asyncio.new_event_loop()
        self.__connector_thread = threading.Thread(
            target=self._mock_server_thread_fn,
            args=(self.__connector_loop,),
        )
        self.__connector_thread.start()

    def stop_connector_thread(self):
        """Stops the mock 'server' and the thread it was on."""
        cancel_loop_tasks(self.__connector_loop)

        # Stop the event loop
        if self.__connector_loop and self.__connector_loop.is_running():
            self.__connector_loop.call_soon_threadsafe(self.__connector_loop.stop)
        self.__connector_thread.join()  # wait for thread to cleanup.
        self.__connector_loop.close()

        self._clear()

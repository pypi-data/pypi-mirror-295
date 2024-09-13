"""Abstract connector class module."""

import asyncio
import ctypes
import threading

from abc import ABC, abstractmethod

from .async_utils import cancel_tasks_in_loop, cancellable

# User friendly error message about there not being a connection when the user
# tries to send data over to the Mission Control app.
SEND_DATA_NOT_CONNECTED_ERROR_MSG = (
    "Tried to send data to the Mission Control app but the connection has been "
    "lost. If you don't see an error in the app, then this is likely due to an "
    "internal issue. Try restarting it to see whether it resolves itself."
)


class Connector(ABC):
    """Abstract class fpr starting and stopping a connector on a separate thread

    This base class takes care of all of the threading logic. To implement it,
    subclasses need to implement 3 async methods:
        - _send_component_data(component)
            -  Args: component: DataSenderComponent whose data will be sent over
        - _start_connector()
        - _stop_connector()
    """

    def __init__(self):
        self.__original_thread = None
        self.__connector_thread = None
        self.__connector_thread_exception = None
        self.__connector_loop = None
        self.__connected_event = threading.Event()

    def __reset(self):
        self.__original_thread = None
        self.__connector_thread = None
        # Note: self.__connector_thread_exception is purposefully not cleared.
        #       It needs to remain so that callers can bubble it up.
        self.__connector_loop = None
        self.__connected_event.clear()

    @property
    def is_connected(self):
        """Indicates whether the connection has been established."""
        return self.__connected_event.is_set()

    @is_connected.setter
    def is_connected(self, connected):
        """Whether the Connector is connected to a client."""
        if connected:
            self.__connected_event.set()
        else:
            # reset connected event
            self.__connected_event = threading.Event()

    @property
    def _original_thread(self):
        return self.__original_thread

    def wait_for_connection(self, timeout=None):
        """Wait for the connection to be established.

        Once a connection has been made, this will return any calls immediately.
        This will keep being the case until the connector is marked as
        disconnected.

        Args:
            - timeout: (default None) The amount of time (in seconds) to wait
                before raising an error.

        Raises:
            TimeoutError: If timeout arg is set and the wait lasts for longer
                than the amount specified.
        """
        if not self.__connected_event.wait(timeout=timeout):
            raise TimeoutError("Timeout waiting for connection")

        if self.__connector_thread_exception:
            # If there was an exception on the thread, then actually there is no
            # connection and it was set to True simply to end the wait. In that
            # case, we reset it now just for correctness.
            self.is_connected = False

    async def _run_coroutine_fn(self, coro_fn, *args, **kwargs):
        try:
            await cancellable(coro_fn)(*args, **kwargs)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self._handle_thread_exception(e)

    @abstractmethod
    async def _send_component_data(self, component):
        """Send component data over to the mission control app."""

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
        if require_connection and not self.is_connected:
            raise RuntimeError(SEND_DATA_NOT_CONNECTED_ERROR_MSG)
        asyncio.run_coroutine_threadsafe(
            self._run_coroutine_fn(self._send_component_data, component),
            self.__connector_loop,
        )

    @abstractmethod
    async def _start_connector(self):
        """Async function that starts the connector.

        This is an async function that should return immediately after starting
        the connector. It should not wait as long as the connection is open
        (e.g. a server should not call `await server.wait_closed()`)
        """

    def _connector_thread_fn(self, loop, connector_ready_event):
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                self._run_coroutine_fn(self._start_connector)
            )
            connector_ready_event.set()
        finally:
            loop.run_forever()

    def start_connector_thread(self):
        """Start the connector on a new separate thread.

        The thread that the connector was started from is stored and accessible
        via `self._original_thread`. The function does not return until the
        connector has been fully started.
        """
        if self.__connector_thread_exception:
            # If there is a thread exception at the start, then it is from a
            # previous attempt. We clear it here so that we are starting fresh.
            self.__connector_thread_exception = None

        self.__original_thread = threading.current_thread()

        def handle_thread_exception(_loop, context):
            exception = context.get("exception", context["message"])
            self._handle_thread_exception(exception)

        # Create a new event loop.
        self.__connector_loop = asyncio.new_event_loop()
        self.__connector_loop.set_exception_handler(handle_thread_exception)
        # Start the event loop in a new thread.
        connector_ready_event = threading.Event()
        self.__connector_thread = threading.Thread(
            target=self._connector_thread_fn,
            args=(self.__connector_loop, connector_ready_event),
        )
        self.__connector_thread.start()

        # Wait until the connector is ready before returning
        connector_ready_event.wait()

    @abstractmethod
    async def _stop_connector(self):
        """Async function used to stop the connector."""

    def _stop_thread(self, num_retries=None, timeout=0.1):
        if not self.__connector_thread.is_alive():
            self.__connector_loop.close()
            return  # Connector thread has stopped and loop is closed. Hooray!

        if num_retries < 0:
            raise RuntimeError("Unable to properly close connection thread.")

        # Try canceling all tasks in the loop and and resolving the thread
        cancel_tasks_in_loop(self.__connector_loop)
        if self.__connector_loop and self.__connector_loop.is_running():
            self.__connector_loop.call_soon_threadsafe(
                self.__connector_loop.stop
            )
        # Wait for thread to cleanup. If it doesn't within the timeout, move on.
        self.__connector_thread.join(timeout=timeout)

        # Verify that the thread is stopped or retry if it is not.
        self._stop_thread(
            num_retries=num_retries - 1 if num_retries is not None else None,
            timeout=timeout,
        )

    def stop_connector_thread(self):
        """Stop the connector and the thread it is on.

        After stopping the connector, all other tasks on the connector thread
        loop are also canceled. Then the thread itself is closed and the class
        instance is reset.
        """
        # Stop the connector on the connector thread.
        future = asyncio.run_coroutine_threadsafe(
            self._stop_connector(), self.__connector_loop
        )
        future.result()

        self._stop_thread(num_retries=5)

        self.__reset()

    def _exit_original_thread(self):
        if self._original_thread is None:
            return  # Nothing to do if we don't know which thread to exit.
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self._original_thread.ident),
            ctypes.py_object(SystemExit),
        )

    def _handle_thread_exception(self, exception):
        # Store the exception which users can access later.
        self.__connector_thread_exception = exception
        # Stop the original thread by sending an interrupt signal.
        self._exit_original_thread()
        # This is a bit of a misapplication but if the error is raised during a
        # wait for connection, we want the program to stop waiting since there
        # is nothing to wait for. So we set is_connected to True (this will be
        # reset immediately after the wait ends). Then the client can handle the
        # error however they choose.
        self.is_connected = True

    def has_thread_exception(self):
        """Whether an exception was raised in the connector thread."""
        return self.__connector_thread_exception is not None

    def raise_thread_exception(self):
        """Raises the exception from the connector thread, if any."""
        if self.has_thread_exception():
            raise self.__connector_thread_exception from None

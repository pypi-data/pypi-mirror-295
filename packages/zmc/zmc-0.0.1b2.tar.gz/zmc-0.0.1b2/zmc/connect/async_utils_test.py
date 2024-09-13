import asyncio
import inspect
import threading
import pytest

from .async_utils import cancellable, cancel_tasks_in_loop


async def async_fn():
    await asyncio.sleep(5)


@cancellable
async def cancellable_async_fn():
    await asyncio.sleep(5)


# TODO: Consider testable thread (for possible exceptions raised). See ref:
#       https://gist.github.com/sbrugman/59b3535ebcd5aa0e2598293cfa58b6ab
@pytest.fixture
def start_thread():

    thread_loop, thread = None, None

    def _start_thread(func):
        nonlocal thread_loop
        nonlocal thread
        thread_loop = asyncio.new_event_loop()
        thread = threading.Thread(target=func, args=(thread_loop,))
        thread.start()
        return thread_loop, thread

    yield _start_thread

    if thread_loop and thread:
        thread_loop.call_soon_threadsafe(thread_loop.stop)
        thread.join()
        thread_loop.close()


@pytest.mark.asyncio
async def test_cancellable_suppresses_error():

    async def run_and_cancel(coro_fn):
        task = asyncio.create_task(coro_fn())
        await asyncio.sleep(0)
        task.cancel()
        await task

    # Confirm CancelledError is raised normally
    with pytest.raises(asyncio.CancelledError):
        await run_and_cancel(async_fn)

    # Cancellable async fn doesn't raise when cancellable.
    await run_and_cancel(cancellable(async_fn))


def test_decorated_fn_still_async():
    assert inspect.iscoroutinefunction(cancellable_async_fn)


def test_decorating_non_async_fn_raises():

    with pytest.raises(ValueError, match="only decorate async functions"):

        @cancellable
        def sync_fn():
            pass  # pragma: no cover


def test_cancel_loop_tasks_different_thread(start_thread):

    def thread_func(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cancellable_async_fn())
        loop.run_forever()

    # Start a new thread with its own event loop running thread_func
    thread_loop, _ = start_thread(thread_func)
    cancel_tasks_in_loop(thread_loop)


# TODO: test cancel tasks
# TODO: test repeat

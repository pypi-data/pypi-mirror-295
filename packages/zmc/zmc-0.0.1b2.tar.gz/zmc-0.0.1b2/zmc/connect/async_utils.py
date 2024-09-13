"""Util functions for async functionality."""

import asyncio
import functools
import inspect
import time


def cancellable(coro_fn):
    """Convenience decorator that makes a coroutine function cancellable."""

    if not inspect.iscoroutinefunction(coro_fn):
        raise ValueError("cancellable can only decorate async functions.")

    @functools.wraps(coro_fn)
    async def cancellable_wrapper(*args, **kwargs):
        try:
            return await coro_fn(*args, **kwargs)
        except asyncio.CancelledError:
            pass  # don't throw anything when canceled.

    return cancellable_wrapper


def cancel_tasks_in_loop(loop):
    """Cancels all tasks in a given loop running on a separate thread.

    If the loop is not running, nothing is done. If it is, then it is assumed
    that it is running on a separate thread.

    Args:
        - loop: asyncio event loop.
    """

    async def cancel_all_tasks():
        # Gather all tasks that are not this current one and cancel them.
        tasks = [
            task
            for task in asyncio.all_tasks(loop)
            if task is not asyncio.current_task()
        ]
        for task in tasks:
            task.cancel()
        # Wait for all tasks to be canceled before returning.
        # TODO: This is maybe a little broken. If the user is using
        #       `run_until_complete` on one of the tasks that is canceled, then
        #       this call will hang.
        await asyncio.gather(*tasks, return_exceptions=True)

    # Only try and cancel tasks if the loop is running.
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(cancel_all_tasks(), loop)
        future.result()


def async_repeat(interval):
    """Convenience decorator that repeats a coroutine at regular intervals.

    The precision of this function is within a few milliseconds of the target
    interval, especially averaged over multiple repetitions.

    Args:
        - interval: How long to wait in between repetitions (in s)
    """

    def repeat_decorator(coro_fn):
        """Convenience decorator that makes a coroutine function cancellable."""

        if not inspect.iscoroutinefunction(coro_fn):
            raise ValueError("async_repeat can only decorate async functions.")

        @functools.wraps(coro_fn)
        async def repeat_wrapper(*args, **kwargs):
            time_delta, start = 0, time.time()
            while True:
                remaining_time = max(interval - time_delta, 0)
                await asyncio.sleep(remaining_time)
                prev_start = start
                start = time.time()
                # Calculate how much longer the wait took compared to the target
                # interval. asyncio.sleep is not extremely precise so this helps
                # keep things more or less accurate over time.
                extra_sleep_delay = start - prev_start - interval
                await coro_fn(*args, **kwargs)
                end = time.time()
                # `time_delta` is however long it has been since the end of the
                # previous sleep call plus however much the previous sleep call
                # overshot the taret interval.
                time_delta = end - start + extra_sleep_delay

        return repeat_wrapper

    return repeat_decorator

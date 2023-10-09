#!/usr/bin/env python3
"""Import wait_random from 0-basic_async_syntax.Write a function
(do not create an async function, use the regular function syntax to do this)
task_wait_random that takes an integer max_delay and returns a asyncio.Task."""

wait_random = __import__('0-basic_async_syntax').wait_random
import asyncio


def task_wait_random(max_delay: int) -> asyncio.tasks:
    """The event loop is responsible for coordinating the execution
    of asynchronous tasks and coroutines.create_task schedules the execution
    of the wait_random coroutine within the event loop and returns a task object
    representing that execution."""
    createLoop = asyncio.get_event_loop()
    theTask = createLoop.create_task(wait_random(max_delay))
    return theTask
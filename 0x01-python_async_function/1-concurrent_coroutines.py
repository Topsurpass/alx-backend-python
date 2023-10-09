#!/usr/bin/env python3
"""This module imports wait_random from the previous python file
that I’ve written and write an async routine called wait_n that
takes in 2 int arguments (in this order): n and max_delay.
You will spawn wait_random n times with the specified max_delay.
wait_n should return the list of all the delays (float values).
The list of the delays should be in ascending order without using
sort() because of concurrency."""

import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """wait_n should return the list of all the delays (float values)
    in order in which and as they are completed"""
    outputList = [wait_random(max_delay) for _ in range(n)]
    result = []
    for task in asyncio.as_completed(outputList):
        delayOrder = await task
        result.append(delayOrder)
    return result

#!/usr/bin/env python3

"""This module contains code that needs to be augmented with the
correct duck-typed annotations"""
from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Afunction that accepts sequence of any type and return either
    of Any types or None"""
    if lst:
        return lst[0]
    else:
        return None

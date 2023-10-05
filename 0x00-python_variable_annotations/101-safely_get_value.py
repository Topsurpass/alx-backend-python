#!/usr/bin/env python3

"""This module contains functions that type annotation is to be added
to using TypeVar.
It accepts a dictionary-like object(mapping)
The key can be any type
default can be of any type specified by T or None
It returns either Any or type T
"""
from typing import TypeVar, Mapping, Any, Union, Optional

T = TypeVar('T')


def safely_get_value(
        dct: Mapping, key: Any, default: Optional[T] = None) -> Union[Any, T]:
    """A function that safely get value from maplike parameters"""
    if key in dct:
        return dct[key]
    else:
        return default

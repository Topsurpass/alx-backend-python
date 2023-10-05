#!/usr/bin/env python3

"""This module tries to annotate the below function’s parameters and
return values with the appropriate types"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Accept iterable and return list of tuples"""
    return [(i, len(i)) for i in lst]

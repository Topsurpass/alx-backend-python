#!/usr/bin/env python3

"""This module contains complex types - mixed list"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ a type-annotated function sum_mixed_list which takes a list
    mxd_lst of integers and floats and returns their sum as a float."""

    total = 0.0

    for i in mxd_lst:
        total += i
    return float(total)

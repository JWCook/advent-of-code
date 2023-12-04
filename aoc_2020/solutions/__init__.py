# ruff: noqa: F401
from aoc_utils import Solution
from aoc_utils import read_input as read_input_generic


def read_input(puzzle_id: int, **kwargs) -> str:
    return read_input_generic(puzzle_id, 2020, **kwargs)

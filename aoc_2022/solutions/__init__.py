# ruff: noqa: F401
from pathlib import Path

from aoc_utils import Solution
from aoc_utils import read_input as read_input_generic

SOLUTIONS_DIR = Path(__file__).parent.parent / 'solutions'


def read_input(puzzle_id: int, **kwargs) -> str:
    return read_input_generic(puzzle_id, 2022, **kwargs)

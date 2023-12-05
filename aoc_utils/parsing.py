"""Utilitiy functions for parsing input data"""
from typing import Iterable

from .utils import BASE_DIR


def chunkify(value: Iterable, size=2) -> list[tuple]:
    """Split an iterable into chunks of a given size"""
    it = iter(value)
    return list(zip(*[it] * size, strict=True))


def read_input(year: int, puzzle_id: int, test: bool = False) -> str:
    inputs_dir = BASE_DIR / f'aoc_{year}' / 'inputs'
    filename = f'input_{puzzle_id:02d}'
    if test:
        filename += '_test'
    return (inputs_dir / filename).read_text()
